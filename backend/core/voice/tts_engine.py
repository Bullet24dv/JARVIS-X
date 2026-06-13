import asyncio
import edge_tts
import io
import soundfile as sf
import numpy as np
from loguru import logger
from backend.config import settings

class TTSEngine:
    def __init__(self):
        self.voice = settings.edge_tts_voice
        self.rate = settings.jarvis_tts_rate
        
    async def synthesize(self, text: str, emotion: str = "neutral") -> np.ndarray:
        """Sintetiza texto a audio (retorna array numpy)"""
        communicate = edge_tts.Communicate(text, self.voice, rate=f"{int(self.rate*100)}+%")
        audio_data = b""
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_data += chunk["data"]
        # Convertir a numpy array (asumiendo 24kHz, mono)
        audio_array, samplerate = sf.read(io.BytesIO(audio_data))
        return audio_array