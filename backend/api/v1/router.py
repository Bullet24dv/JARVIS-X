from fastapi import APIRouter
from backend.api.v1.endpoints import chat, voice, vision, computer, agents, memory, mcp, telegram, system

api_router = APIRouter()

api_router.include_router(chat.router, prefix="/chat", tags=["Chat"])
api_router.include_router(voice.router, prefix="/voice", tags=["Voice"])
api_router.include_router(vision.router, prefix="/vision", tags=["Vision"])
api_router.include_router(computer.router, prefix="/computer", tags=["Computer"])
api_router.include_router(agents.router, prefix="/agents", tags=["Agents"])
api_router.include_router(memory.router, prefix="/memory", tags=["Memory"])
api_router.include_router(mcp.router, prefix="/mcp", tags=["MCP"])
api_router.include_router(telegram.router, prefix="/telegram", tags=["Telegram"])
api_router.include_router(system.router, prefix="/system", tags=["System"])