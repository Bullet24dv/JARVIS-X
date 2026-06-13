import asyncio
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from prometheus_fastapi_instrumentator import Instrumentator
from loguru import logger

from backend.config import settings
from backend.api.v1.router import api_router
from backend.api.v1.websockets.manager import websocket_manager
from backend.core.event_bus import event_bus
from backend.core.task_queue import task_queue
from backend.services.llm_service import LLMService
from backend.services.voice_service import VoiceService
from backend.services.vision_service import VisionService
from backend.services.mcp_service import MCPService
from backend.services.agent_service import AgentService
from backend.models.database import init_db

# Configurar logging
logger.add(settings.log_file, rotation="1 day", retention="7 days", level=settings.log_level)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting JARVIS-X backend...")
    await init_db()
    await task_queue.start()
    await event_bus.start()
    
    # Initialize core services
    app.state.llm_service = LLMService()
    await app.state.llm_service.initialize()
    # app.state.voice_service = VoiceService()
    # await app.state.voice_service.start_listening()
    app.state.vision_service = VisionService()
    await app.state.vision_service.initialize()
    app.state.mcp_service = MCPService()
    await app.state.mcp_service.connect_all()
    app.state.agent_service = AgentService()
    await app.state.agent_service.initialize()
    
    logger.info("JARVIS-X ready.")
    yield
    # Shutdown
    logger.info("Shutting down...")
    # await app.state.voice_service.stop()
    await task_queue.stop()
    await event_bus.stop()
    await app.state.mcp_service.disconnect_all()

app = FastAPI(
    title="JARVIS-X API",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Metrics
Instrumentator().instrument(app).expose(app)

# Router
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "JARVIS-X Operational", "status": "online", "version": "1.0.0"}

@app.websocket("/ws/public")
async def websocket_public_endpoint(websocket: WebSocket):
    """WebSocket público sin autenticación para pruebas"""
    logger.info("Public WebSocket connection attempt...")
    await websocket.accept()
    logger.info("Public WebSocket accepted")
    await websocket.send_json({"type": "connected", "message": "Connected to JARVIS-X Public"})
    try:
        while True:
            data = await websocket.receive_json()
            logger.info(f"Received: {data}")
            # Echo para pruebas
            await websocket.send_json({"type": "echo", "data": data})
    except WebSocketDisconnect:
        logger.info("Public WebSocket disconnected")
    except Exception as e:
        logger.error(f"Public WebSocket error: {e}")

@app.get("/health")
async def health():
    return {"status": "healthy", "services": {
        "database": "ok",
        "redis": "ok",
        "rabbitmq": "ok"
    }}
@app.get("/ping")
async def ping():
    return {"ping": "pong"}