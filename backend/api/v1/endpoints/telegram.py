from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from backend.services.telegram_service import TelegramService

router = APIRouter()
telegram_service = TelegramService()

class SendMessageRequest(BaseModel):
    chat_id: int
    text: str

@router.post("/send")
async def send_telegram_message(request: SendMessageRequest):
    await telegram_service.send_message(request.chat_id, request.text)
    return {"status": "sent"}

@router.get("/status")
async def telegram_status():
    return {"connected": telegram_service.is_connected()}