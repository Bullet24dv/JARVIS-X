from faster_whisper import WhisperModel
import numpy as np
from loguru import logger

class FasterWhisperSTT:
    def __init__(self, model_size="base", device="cpu", compute_type="int8"):
        self.model = None
        self.model_size = model_size
        self.device = device
        self.compute_type = compute_type
        
    async def initialize(self):
        self.model = WhisperModel(self.model_size, device=self.device, compute_type=self.compute_type)
        logger.info("FasterWhisper STT initialized")
        
    async def transcribe(self, audio_bytes: bytes, language: str = "es") -> str:
        if not self.model:
            await self.initialize()
        audio_array = np.frombuffer(audio_bytes, dtype=np.int16).astype(np.float32) / 32768.0
        segments, _ = self.model.transcribe(audio_array, language=language, beam_size=5)
        return " ".join(seg.text for seg in segments)