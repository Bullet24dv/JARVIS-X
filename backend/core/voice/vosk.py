import json
import vosk
import wave
import numpy as np
from loguru import logger

class VoskSTT:
    def __init__(self, model_path="models/vosk-small-es"):
        self.model = None
        self.rec = None
        self.model_path = model_path
        
    async def initialize(self):
        self.model = vosk.Model(self.model_path)
        self.rec = vosk.KaldiRecognizer(self.model, 16000)
        logger.info("Vosk STT initialized")
        
    async def transcribe(self, audio_bytes: bytes) -> str:
        if not self.rec:
            await self.initialize()
        if self.rec.AcceptWaveform(audio_bytes):
            result = json.loads(self.rec.Result())
            return result.get("text", "")
        return ""