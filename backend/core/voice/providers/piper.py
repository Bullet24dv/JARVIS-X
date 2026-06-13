import subprocess
import tempfile
import numpy as np
from loguru import logger

class PiperTTS:
    def __init__(self, model_path="models/piper/es_ES-dave-medium.onnx"):
        self.model_path = model_path
        
    async def synthesize(self, text: str) -> np.ndarray:
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            cmd = ["piper", "--model", self.model_path, "--output_file", tmp.name, "--sentence", text]
            result = subprocess.run(cmd, capture_output=True)
            if result.returncode != 0:
                logger.error(f"Piper error: {result.stderr}")
                return np.zeros(0)
            import soundfile as sf
            audio, _ = sf.read(tmp.name)
            return audio