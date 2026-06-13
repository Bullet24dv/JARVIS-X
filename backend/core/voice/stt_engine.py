import asyncio
import numpy as np
from faster_whisper import WhisperModel
from loguru import logger
import os

class STTEngine:
    def __init__(self, model_size="base", device="cpu", compute_type="int8"):
        self.model_size = model_size
        self.device = device
        self.compute_type = compute_type
        self.model = None
        
    async def initialize(self):
        """Inicializa el modelo de transcripción"""
        self.model = WhisperModel(self.model_size, device=self.device, compute_type=self.compute_type)
        logger.info("STT Engine initialized with Faster Whisper")
        
    async def transcribe(self, audio_bytes: bytes, language: str = "es") -> str:
        """Transcribe audio a texto"""
        if not self.model:
            await self.initialize()
        # Convertir bytes a numpy array (asumiendo 16kHz mono 16-bit)
        audio_array = np.frombuffer(audio_bytes, dtype=np.int16).astype(np.float32) / 32768.0
        segments, info = self.model.transcribe(audio_array, language=language, beam_size=5)
        result = " ".join(seg.text for seg in segments)
        return result.strip()