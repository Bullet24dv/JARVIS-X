from openai import AsyncOpenAI
from backend.config import settings
import numpy as np
import io
import soundfile as sf

class OpenAITTS:
    @staticmethod
    async def synthesize(text: str) -> np.ndarray:
        client = AsyncOpenAI(api_key=settings.openai_api_key)
        response = await client.audio.speech.create(
            model="tts-1",
            voice="alloy",
            input=text
        )
        audio_bytes = await response.aread()
        audio_array, _ = sf.read(io.BytesIO(audio_bytes))
        return audio_array