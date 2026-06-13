import aiohttp
from backend.config import settings
from loguru import logger

class FishAudioTTS:
    @staticmethod
    async def synthesize(text: str) -> bytes:
        url = "https://api.fish.audio/v1/tts"
        headers = {"Authorization": f"Bearer {settings.fish_audio_api_key}"}
        payload = {"text": text, "voice": "jarvis", "format": "wav"}
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload, headers=headers) as resp:
                if resp.status != 200:
                    logger.error(f"FishAudio error: {await resp.text()}")
                    return b""
                return await resp.read()