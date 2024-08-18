import logging
import os

from achatbot.common.types import MODELS_DIR, SileroVADArgs, WebRTCVADArgs
from achatbot.common import interface
from achatbot.common.factory import EngineClass, EngineFactory

from dotenv import load_dotenv
load_dotenv(override=True)


class VADEnvInit():

    @staticmethod
    def getEngine(tag, **kwargs) -> interface.IDetector | EngineClass:
        if "pyannote_" in tag:
            from . import pyannote
        elif "webrtc_" in tag:
            from . import webrtc_vad
        elif "webrtc_silero_" in tag:
            from . import webrtc_silero_vad
        elif "silero_" in tag:
            from . import silero_vad

        engine = EngineFactory.get_engine_by_tag(EngineClass, tag, **kwargs)
        return engine

    @staticmethod
    def initVADEngine() -> interface.IDetector | EngineClass:
        # vad detector
        tag = os.getenv('VAD_DETECTOR_TAG', "silero_vad")
        kwargs = VADEnvInit.map_config_func[tag]()
        engine = VADEnvInit.getEngine(tag, **kwargs)
        logging.info(f"initVADEngine: {tag}, {engine}")
        return engine

    @staticmethod
    def get_pyannote_vad_args() -> dict:
        model_type = os.getenv(
            'VAD_MODEL_TYPE', 'segmentation-3.0')
        model_ckpt_path = os.path.join(
            MODELS_DIR, 'pyannote', model_type, "pytorch_model.bin")
        kwargs = {}
        kwargs["path_or_hf_repo"] = os.getenv(
            'VAD_PATH_OR_HF_REPO', model_ckpt_path)
        kwargs["model_type"] = model_type
        return kwargs

    @staticmethod
    def get_silero_vad_args() -> dict:
        kwargs = SileroVADArgs(
            sample_rate=int(os.getenv('SAMPLE_RATE', "16000")),
            force_reload=bool(os.getenv('FORCE_RELOAD', "")),
            is_pad_tensor=bool(os.getenv('IS_PAD_TENSOR', "1")),
            onnx=bool(os.getenv('ONNX', "")),
            repo_or_dir=os.getenv('REPO_OR_DIR', "snakers4/silero-vad"),
            model=os.getenv('SILERO_MODEL', "silero_vad"),
            check_frames_mode=int(os.getenv('CHECK_FRAMES_MODE', "1")),
        ).__dict__
        return kwargs

    @staticmethod
    def get_webrtc_vad_args() -> dict:
        kwargs = WebRTCVADArgs(
            aggressiveness=int(os.getenv('AGGRESSIVENESS', "1")),
            check_frames_mode=int(os.getenv('CHECK_FRAMES_MODE', "1")),
        ).__dict__
        return kwargs

    @staticmethod
    def get_webrtc_silero_vad_args() -> dict:
        return {**VADEnvInit.get_webrtc_vad_args(), **VADEnvInit.get_silero_vad_args()}

    # TAG : config
    map_config_func = {
        'silero_vad': get_silero_vad_args,
        'webrtc_vad': get_webrtc_vad_args,
        'webrtc_silero_vad': get_webrtc_silero_vad_args,
        'pyannote_vad': get_pyannote_vad_args,
    }


class WakerEnvInit():
    @staticmethod
    def initWakerEngine() -> interface.IDetector | EngineClass:
        from . import porcupine
        # waker
        recorder_tag = os.getenv('RECORDER_TAG', "rms_recorder")
        if "wake" not in recorder_tag:
            return None

        tag = os.getenv('WAKER_DETECTOR_TAG', "porcupine_wakeword")
        wake_words = os.getenv('WAKE_WORDS', "小黑")
        model_path = os.path.join(
            MODELS_DIR, "porcupine_params_zh.pv")
        keyword_paths = os.path.join(
            MODELS_DIR, "小黑_zh_mac_v3_0_0.ppn")
        kwargs = {}
        kwargs["wake_words"] = wake_words
        kwargs["keyword_paths"] = os.getenv(
            'KEYWORD_PATHS', keyword_paths).split(',')
        kwargs["model_path"] = os.getenv('MODEL_PATH', model_path)
        engine = EngineFactory.get_engine_by_tag(EngineClass, tag, **kwargs)
        return engine
