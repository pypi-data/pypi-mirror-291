from concurrent.futures import ThreadPoolExecutor
from queue import Queue
from typing import Generator

from achatbot.common.session import Session
from achatbot.common.factory import EngineClass
from achatbot.types.speech.asr.base import ASRArgs
from achatbot.common.utils import task
from achatbot.common.interface import IAsr


class ASRBase(EngineClass, IAsr):
    @classmethod
    def get_args(cls, **kwargs) -> dict:
        return {**ASRArgs().__dict__, **kwargs}

    def __init__(self, **args) -> None:
        self.args = ASRArgs(**args)
        self.asr_audio = None

    def transcribe_stream_sync(self, session: Session) -> Generator[str, None, None]:
        queue: Queue = Queue()
        with ThreadPoolExecutor() as executor:
            executor.submit(task.fetch_async_items, queue, self.transcribe_stream, session)
            while True:
                item = queue.get()
                if item is None:
                    break
                yield item
