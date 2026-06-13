"""
Piper TTS Provider (opcional, requiere instalación separada)
"""

import subprocess
import tempfile
import numpy as np
from loguru import logger


class PiperTTS:
    def __init__(self, model_path: str = "models/piper/es_ES-dave-medium.onnx"):
        self.model_path = model_path
        
    async def initialize(self) -> bool:
        # Verificar si piper está instalado
        try:
            result = subprocess.run(["piper", "--help"], capture_output=True)
            return result.returncode == 0
        except FileNotFoundError:
            logger.warning("Piper not installed. Skipping.")
            return False
    
    async def synthesize(self, text: str) -> np.ndarray:
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            cmd = ["piper", "--model", self.model_path, "--output_file", tmp.name]
            subprocess.run(cmd + [text], capture_output=True)
            import soundfile as sf
            audio, sr = sf.read(tmp.name)
            return audio