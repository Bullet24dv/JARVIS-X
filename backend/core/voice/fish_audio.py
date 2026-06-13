"""
Fish Audio TTS Provider for JARVIS-X
"""

import aiohttp
from typing import Optional
from loguru import logger
from backend.config import settings


class FishAudioTTS:
    def __init__(self):
        self.api_key = settings.fish_audio_api_key
        self.base_url = "https://api.fish.audio/v1"
        self.session = None
        self.available = False
        
    async def initialize(self) -> bool:
        if not self.api_key:
            logger.warning("Fish Audio API key not configured")
            return False
        self.session = aiohttp.ClientSession()
        self.available = True
        logger.info("Fish Audio TTS initialized")
        return True
    
    async def synthesize(self, text: str, voice_id: str = "jarvis") -> bytes:
        if not self.available:
            raise Exception("Fish Audio not initialized")
        
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        payload = {"text": text, "voice": voice_id, "format": "wav"}
        
        async with self.session.post(f"{self.base_url}/tts", json=payload, headers=headers) as resp:
            if resp.status != 200:
                logger.error(f"Fish Audio error: {await resp.text()}")
                return b""
            return await resp.read()
    
    async def close(self):
        if self.session:
            await self.session.close()
            self.available = False