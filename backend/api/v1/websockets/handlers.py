from backend.api.v1.websockets.manager import websocket_manager
from loguru import logger

async def broadcast_agent_status(agent_name: str, status: str):
    await websocket_manager.send_message({
        "type": "agent_status",
        "agent": agent_name,
        "status": status
    })

async def broadcast_voice_response(text: str):
    await websocket_manager.send_message({
        "type": "voice_response",
        "text": text
    })