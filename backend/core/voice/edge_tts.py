"""
Edge TTS Provider for JARVIS-X (gratuito, sin API key)
"""

import edge_tts
import io
import soundfile as sf
import numpy as np
from backend.config import settings


class EdgeTTSTTS:
    @staticmethod
    async def synthesize(text: str, voice: str = None) -> np.ndarray:
        voice = voice or settings.edge_tts_voice
        rate = f"{int(settings.jarvis_tts_rate * 100)}+%"
        communicate = edge_tts.Communicate(text, voice, rate=rate)
        
        audio_data = b""
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_data += chunk["data"]
        
        audio_array, samplerate = sf.read(io.BytesIO(audio_data))
        return audio_array