from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
from backend.services.voice_service import VoiceService
import base64

router = APIRouter()

class TextToSpeechRequest(BaseModel):
    text: str
    emotion: str = "neutral"

@router.post("/tts")
async def text_to_speech(request: TextToSpeechRequest):
    voice_service = VoiceService()
    audio = await voice_service.speak(request.text, request.emotion)
    return {"audio": base64.b64encode(audio).decode()}

@router.websocket("/stt")
async def speech_to_text(websocket: WebSocket):
    await websocket.accept()
    voice_service = VoiceService()
    try:
        while True:
            audio_data = await websocket.receive_bytes()
            text = await voice_service.stt.transcribe(audio_data)
            await websocket.send_json({"text": text})
    except WebSocketDisconnect:
        pass