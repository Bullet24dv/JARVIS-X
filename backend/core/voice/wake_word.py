import numpy as np
import webrtcvad
import collections
from loguru import logger

class WakeWordDetector:
    def __init__(self, mode=3, frame_duration_ms=30, padding_ms=300, ratio=0.5):
        self.vad = webrtcvad.Vad(mode)
        self.frame_duration_ms = frame_duration_ms
        self.padding_ms = padding_ms
        self.ratio = ratio
        self.num_padding_frames = padding_ms // frame_duration_ms
        self.ring_buffer = collections.deque(maxlen=self.num_padding_frames)
        self.triggered = False
        
    async def detect(self, audio_chunk: np.ndarray) -> bool:
        """Detecta si hay voz hablada"""
        try:
            # Asegurar formato correcto (int16, 16kHz, mono)
            if audio_chunk.dtype != np.int16:
                audio_chunk = (audio_chunk * 32767).astype(np.int16)
            
            # Asegurar longitud correcta (30ms = 480 samples a 16kHz)
            expected_length = int(16000 * self.frame_duration_ms / 1000)
            if len(audio_chunk) < expected_length:
                return False
            
            # Tomar frame de tamaño correcto
            frame = audio_chunk[:expected_length].tobytes()
            is_speech = self.vad.is_speech(frame, sample_rate=16000)
            
            self.ring_buffer.append(is_speech)
            num_voiced = sum(self.ring_buffer)
            
            if not self.triggered and num_voiced > self.ratio * self.ring_buffer.maxlen:
                self.triggered = True
                return True
            elif self.triggered and num_voiced == 0:
                self.triggered = False
            return False
        except Exception as e:
            logger.error(f"VAD error: {e}")
            return False