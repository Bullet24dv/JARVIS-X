import noisereduce as nr
import numpy as np

class NoiseReducer:
    def __init__(self, stationary=True, prop_decrease=1.0):
        self.stationary = stationary
        self.prop_decrease = prop_decrease
        
    def reduce(self, audio: np.ndarray, sample_rate: int = 16000) -> np.ndarray:
        """Reduce ruido de fondo"""
        if len(audio) > sample_rate * 0.5:  # Tomar un segmento de ruido al inicio
            noise_clip = audio[:int(sample_rate * 0.3)]
            reduced = nr.reduce_noise(y=audio, sr=sample_rate, y_noise=noise_clip, prop_decrease=self.prop_decrease, stationary=self.stationary)
        else:
            reduced = audio
        return reduced