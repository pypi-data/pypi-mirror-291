import logging
import json

import grpc
import uuid

from achatbot.common.grpc.idl.tts_pb2_grpc import TTSServicer
from achatbot.common.grpc.idl.tts_pb2 import (
    LoadModelRequest, LoadModelResponse,
    SynthesizeRequest, SynthesizeResponse,
)
from achatbot.common.factory import EngineFactory, EngineClass
from achatbot.common.session import Session
from achatbot.common.types import SessionCtx, ITts
import achatbot.modules.speech.tts


def get_session_id(context: grpc.ServicerContext):
    for item in context.invocation_metadata():
        if item.key == "client_id":
            return item.value
    return str(uuid.uuid4())


class TTS(TTSServicer):
    def __init__(self,) -> None:
        super().__init__()
        self.tts = None

    def LoadModel(self, request: LoadModelRequest, context: grpc.ServicerContext):
        logging.debug(f"LoadModel request: {request}")
        kwargs = json.loads(request.json_kwargs)
        logging.debug(f"LoadModel kwargs: {kwargs}")
        if self.tts is not None and request.is_reload == False:
            logging.debug(f"Already initialized {self.tts.TAG} args: {self.tts.args} -> {self.tts}")
            return LoadModelResponse()
        self.tts: EngineClass | ITts = EngineFactory.get_engine_by_tag(
            EngineClass, request.tts_tag, **kwargs)
        logging.debug(f"init {self.tts.TAG} args:{self.tts.args} -> {self.tts}")
        return LoadModelResponse()

    def SynthesizeUS(self,
                     request: SynthesizeRequest,
                     context: grpc.ServicerContext):
        logging.debug(f"SynthesizeUS request: {request}")
        self.session = Session(**SessionCtx(get_session_id(context)).__dict__)
        self.session.ctx.state["tts_text"] = request.tts_text
        iter = self.tts.synthesize_sync(self.session)
        for i, chunk in enumerate(iter):
            logging.debug(f"get {i} chunk {len(chunk)}")
            yield SynthesizeResponse(tts_audio=chunk)
