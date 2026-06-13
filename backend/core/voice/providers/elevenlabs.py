import requests
from backend.config import settings
from loguru import logger

class ElevenLabsTTS:
    @staticmethod
    async def synthesize(text: str) -> bytes:
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{settings.elevenlabs_voice_id}"
        headers = {
            "xi-api-key": settings.elevenlabs_api_key,
            "Content-Type": "application/json"
        }
        data = {
            "text": text,
            "voice_settings": {"stability": 0.5, "similarity_boost": 0.75}
        }
        response = requests.post(url, json=data, headers=headers)
        if response.status_code != 200:
            logger.error(f"ElevenLabs error: {response.text}")
            return b""
        return response.content