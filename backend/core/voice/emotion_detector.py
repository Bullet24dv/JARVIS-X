import numpy as np
from scipy.signal import find_peaks

class EmotionDetector:
    """Detector simple de emociones por tono y energía"""
    
    async def detect(self, audio: np.ndarray, sample_rate: int = 16000) -> str:
        # Calcular energía RMS
        rms = np.sqrt(np.mean(audio**2))
        # Calcular pitch (frecuencia fundamental estimada)
        autocorr = np.correlate(audio, audio, mode='full')
        autocorr = autocorr[len(autocorr)//2:]
        peaks, _ = find_peaks(autocorr, height=0.5*np.max(autocorr))
        if len(peaks) > 0:
            pitch = sample_rate / peaks[0]
        else:
            pitch = 0
            
        if rms > 0.1 and pitch > 200:
            return "excited"
        elif rms > 0.05 and pitch < 120:
            return "calm"
        elif rms < 0.02:
            return "sad"
        else:
            return "neutral"