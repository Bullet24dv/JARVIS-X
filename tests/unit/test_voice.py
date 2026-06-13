import pytest
from backend.core.voice.stt_engine import STTEngine

@pytest.mark.asyncio
async def test_stt():
    stt = STTEngine()
    await stt.initialize()
    # Mock audio test
    result = await stt.transcribe(b"")
    assert result is not None