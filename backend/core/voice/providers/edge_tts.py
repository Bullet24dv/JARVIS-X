import edge_tts
import io
import soundfile as sf
import numpy as np
from backend.config import settings

class EdgeTTSTTS:
    @staticmethod
    async def synthesize(text: str) -> np.ndarray:
        communicate = edge_tts.Communicate(text, settings.edge_tts_voice, rate=f"{int(settings.jarvis_tts_rate*100)}+%")
        audio_data = b""
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_data += chunk["data"]
        audio_array, _ = sf.read(io.BytesIO(audio_data))
        return audio_array