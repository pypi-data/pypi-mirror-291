import logging
from typing import AsyncGenerator
import random
import io
import os

from pydub import AudioSegment

from achatbot.common.interface import ITts
from achatbot.common.session import Session
from achatbot.common.types import EdgeTTSArgs, RECORDS_DIR, EDGE_TTS_SYNTHESIS_FILE
from .base import BaseTTS


class EdgeTTS(BaseTTS, ITts):
    TAG = "tts_edge"

    @classmethod
    def get_args(cls, **kwargs) -> dict:
        return {**EdgeTTSArgs().__dict__, **kwargs}

    def __init__(self, **args) -> None:
        self.args = EdgeTTSArgs(**args)
        self.file_path = os.path.join(RECORDS_DIR, EDGE_TTS_SYNTHESIS_FILE)

    async def _inference(self, session: Session, text: str) -> AsyncGenerator[bytes, None]:
        import edge_tts

        if self.args.voice_name:
            voices = await self.get_voices(ShortName=self.args.voice_name)
            logging.debug(f"{self.TAG} voices: {voices}")
            if len(voices) == 0:
                raise Exception(
                    f"{self.TAG} voice:{self.args.voice_name} don't support")
        else:
            voices = self.get_voices(
                Gender=self.args.gender, Language=self.args.language)
            self.args.voice_name = random.choice(voices)["Name"]

        communicate: edge_tts.Communicate = edge_tts.Communicate(
            text,
            self.args.voice_name,
            rate=self.args.rate,
            volume=self.args.volume,
            pitch=self.args.pitch,
        )
        self.submaker = edge_tts.SubMaker()
        # "outputFormat":"audio-24khz-48kbitrate-mono-mp3"

        with io.BytesIO() as f:
            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    f.write(chunk['data'])
                elif chunk["type"] == "WordBoundary":
                    # logging.info( f"{self.TAG} type:{chunk['type']} chunk: {chunk}")
                    self.submaker.create_sub(
                        (chunk["offset"], chunk["duration"]), chunk["text"])

            f.seek(0)
            audio: AudioSegment = AudioSegment.from_mp3(f)
            audio_resampled = audio.set_frame_rate(
                22050).set_channels(
                1).set_sample_width(2)  # 16bit sample_width 16/8=2
            audio_data = audio_resampled.raw_data
            yield audio_data

    async def get_voices(self, **kwargs):
        from edge_tts import VoicesManager
        voice_mg: VoicesManager = await VoicesManager.create()
        return voice_mg.find(**kwargs)

    async def save_submakers(self, vit_file: str):
        with open(vit_file, "w", encoding="utf-8") as file:
            file.write(self.submaker.generate_subs())
