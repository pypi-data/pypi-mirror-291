import logging
import asyncio
import time
from typing import Any

from apipeline.frames.base import Frame
from apipeline.frames.control_frames import StartFrame
from apipeline.processors.frame_processor import FrameDirection

from achatbot.processors.audio_input_processor import AudioVADInputProcessor
from achatbot.services.daily_client import DailyTransportClient
from achatbot.types.frames.data_frames import (
    InterimTranscriptionFrame,
    TranscriptionFrame,
    UserImageRawFrame
)
from achatbot.types.frames.control_frames import UserImageRequestFrame
from achatbot.common.types import DailyParams
from achatbot.types.frames.data_frames import DailyTransportMessageFrame


class DailyInputTransportProcessor(AudioVADInputProcessor):

    def __init__(self, client: DailyTransportClient, params: DailyParams, **kwargs):
        super().__init__(params, **kwargs)

        self._client = client

        self._video_renderers = {}

    async def start(self, frame: StartFrame):
        # Parent start.
        await super().start(frame)
        # Join the room.
        await self._client.join()
        # Create audio task. It reads audio frames from Daily and push them
        # internally for VAD processing.
        if self._params.audio_in_enabled or self._params.vad_enabled:
            self._audio_in_task = self.get_event_loop().create_task(self._audio_in_task_handler())

    async def stop(self):
        # Parent stop.
        await super().stop()
        # Leave the room.
        await self._client.leave()
        # Stop audio thread.
        if self._params.audio_in_enabled or self._params.vad_enabled:
            self._audio_in_task.cancel()
            await self._audio_in_task

    async def cleanup(self):
        await super().cleanup()
        await self._client.cleanup()

    #
    # FrameProcessor
    #

    async def process_frame(self, frame: Frame, direction: FrameDirection):
        await super().process_frame(frame, direction)

        if isinstance(frame, UserImageRequestFrame):
            self.request_participant_image(frame.user_id)

    #
    # Frames
    #

    async def push_transcription_frame(self, frame: TranscriptionFrame | InterimTranscriptionFrame):
        await self.queue_frame(frame)

    async def push_app_message(self, message: Any, sender: str):
        frame = DailyTransportMessageFrame(message=message, participant_id=sender)
        await self.queue_frame(frame)

    #
    # Audio in
    #

    async def _audio_in_task_handler(self):
        while True:
            try:
                frame = await self._client.read_next_audio_frame()
                if frame:
                    await self.push_audio_frame(frame)
            except asyncio.CancelledError:
                break

    #
    # Camera in
    #

    def capture_participant_video(
            self,
            participant_id: str,
            framerate: int = 30,
            video_source: str = "camera",
            color_format: str = "RGB"):
        self._video_renderers[participant_id] = {
            "framerate": framerate,
            "timestamp": 0,
            "render_next_frame": False,
        }

        self._client.capture_participant_video(
            participant_id,
            self._on_participant_video_frame,
            framerate,
            video_source,
            color_format
        )

    def request_participant_image(self, participant_id: str):
        if participant_id in self._video_renderers:

            self._video_renderers[participant_id]["render_next_frame"] = True

    async def _on_participant_video_frame(self, participant_id: str, buffer, size, format):
        render_frame = False

        curr_time = time.time()
        prev_time = self._video_renderers[participant_id]["timestamp"] or curr_time
        framerate = self._video_renderers[participant_id]["framerate"]

        if framerate > 0:
            next_time = prev_time + 1 / framerate
            render_frame = (curr_time - next_time) < 0.1
        elif self._video_renderers[participant_id]["render_next_frame"]:
            self._video_renderers[participant_id]["render_next_frame"] = False
            render_frame = True

        if render_frame:
            frame = UserImageRawFrame(
                user_id=participant_id,
                image=buffer,
                size=size,
                format=format)
            await self.queue_frame(frame)

        self._video_renderers[participant_id]["timestamp"] = curr_time
