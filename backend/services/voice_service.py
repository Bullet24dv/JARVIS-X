from backend.core.voice.stt_engine import STTEngine
from backend.core.voice.tts_engine import TTSEngine
from backend.core.voice.wake_word import WakeWordDetector
from backend.core.voice.noise_cancel import NoiseReducer
from backend.core.event_bus import event_bus
import numpy as np
import sounddevice as sd
from queue import Queue
import asyncio
from loguru import logger

class VoiceService:
    def __init__(self):
        self.stt = STTEngine()
        self.tts = TTSEngine()
        self.wake_word = WakeWordDetector()
        self.noise_reducer = NoiseReducer()
        self.audio_queue = Queue()
        self.is_listening = False
        self.stream = None
        
    async def initialize(self):
        await self.stt.initialize()
        
    async def start_listening(self):
        self.is_listening = True
        self.stream = sd.InputStream(
            callback=self._audio_callback,
            samplerate=16000,
            channels=1,
            blocksize=1024
        )
        self.stream.start()
        asyncio.create_task(self._process_audio_loop())
        logger.info("Voice service listening...")
        
    def _audio_callback(self, indata, frames, time, status):
        if status:
            logger.warning(f"Audio status: {status}")
        self.audio_queue.put(indata.copy())
        
    async def _process_audio_loop(self):
        while self.is_listening:
            if not self.audio_queue.empty():
                audio_chunk = self.audio_queue.get()
                cleaned = self.noise_reducer.reduce(audio_chunk.flatten())
                if await self.wake_word.detect(cleaned):
                    logger.info("Wake word detected!")
                    # Aquí se grabaría hasta silencio y se transcribiría
                    await event_bus.emit("voice_command", {"text": "comando pendiente"})
            await asyncio.sleep(0.01)
            
    async def speak(self, text: str, emotion: str = "neutral") -> np.ndarray:
        audio = await self.tts.synthesize(text, emotion)
        sd.play(audio, samplerate=24000)
        sd.wait()
        return audio
        
    async def stop(self):
        self.is_listening = False
        if self.stream:
            self.stream.stop()