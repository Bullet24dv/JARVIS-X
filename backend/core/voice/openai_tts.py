"""
OpenAI TTS Provider for JARVIS-X
"""

from openai import AsyncOpenAI
from backend.config import settings
import numpy as np
import io
import soundfile as sf


class OpenAITTS:
    def __init__(self):
        self.client = None
        
    async def initialize(self):
        if settings.openai_api_key:
            self.client = AsyncOpenAI(api_key=settings.openai_api_key)
            return True
        return False
    
    async def synthesize(self, text: str, voice: str = "alloy") -> np.ndarray:
        if not self.client:
            raise Exception("OpenAI not initialized")
        
        response = await self.client.audio.speech.create(
            model="tts-1", voice=voice, input=text
        )
        audio_bytes = await response.aread()
        audio_array, samplerate = sf.read(io.BytesIO(audio_bytes))
        return audio_array