import asyncio
from backend.core.voice.stt_engine import STTEngine
from backend.core.voice.tts_engine import TTSEngine
from loguru import logger

class VoiceWorker:
    def __init__(self):
        self.stt = STTEngine()
        self.tts = TTSEngine()
        
    async def start(self):
        await self.stt.initialize()
        logger.info("Voice worker started")
        
    async def process_audio(self, audio_bytes: bytes) -> str:
        text = await self.stt.transcribe(audio_bytes)
        return text
        
    async def synthesize(self, text: str) -> bytes:
        audio = await self.tts.synthesize(text)
        return audio