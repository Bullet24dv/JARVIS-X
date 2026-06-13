# ============================================================
# JARVIS-X | backend/main.py
# Punto de entrada del servidor FastAPI
# ============================================================

import asyncio
import logging
import sys
import time
from contextlib import asynccontextmanager
from pathlib import Path
from typing import AsyncGenerator

import uvicorn
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from backend.config import settings
from backend.core.database import init_db, close_db
from backend.core.cache import init_cache, close_cache
from backend.core.memory.manager import MemoryManager
from backend.core.llm_router import LLMRouter
from backend.core.agents.orchestrator import AgentOrchestrator
from backend.core.websocket_manager import WebSocketManager
from backend.core.voice.pipeline import VoicePipeline
from backend.api.v1 import router as api_v1_router
from backend.api.ws import router as ws_router

# ── Logging ───────────────────────────────────────────────────
Path("logs").mkdir(exist_ok=True)
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(settings.LOG_FILE, encoding="utf-8"),
    ],
)
logger = logging.getLogger("jarvis.main")

# ── Instancias globales ───────────────────────────────────────
ws_manager = WebSocketManager()
memory_manager: MemoryManager | None = None
llm_router: LLMRouter | None = None
orchestrator: AgentOrchestrator | None = None
voice_pipeline: VoicePipeline | None = None


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Ciclo de vida completo de la aplicación."""
    global memory_manager, llm_router, orchestrator, voice_pipeline

    logger.info("╔══════════════════════════════════════════╗")
    logger.info("║   JARVIS-X  Sistema Operativo IA v2.0   ║")
    logger.info("╚══════════════════════════════════════════╝")
    logger.info("Iniciando subsistemas...")

    # Asegurar directorios
    for d in ["data", "data/chroma", "data/starcars/photos", "data/starcars/output",
              "logs", "models", "uploads"]:
        Path(d).mkdir(parents=True, exist_ok=True)

    # Base de datos
    logger.info("[1/6] Inicializando bases de datos...")
    await init_db()

    # Cache Redis
    logger.info("[2/6] Conectando a Redis...")
    await init_cache()

    # Memoria
    logger.info("[3/6] Cargando sistema de memoria...")
    memory_manager = MemoryManager()
    await memory_manager.initialize()
    app.state.memory = memory_manager

    # Router LLM
    logger.info("[4/6] Configurando router de modelos IA...")
    llm_router = LLMRouter()
    await llm_router.initialize()
    app.state.llm = llm_router

    # Orquestador de agentes
    logger.info("[5/6] Iniciando orquestador multiagente...")
    orchestrator = AgentOrchestrator(llm_router=llm_router, memory=memory_manager)
    await orchestrator.initialize()
    app.state.orchestrator = orchestrator

    # Pipeline de voz (opcional, no bloquea)
    logger.info("[6/6] Preparando pipeline de voz...")
    try:
        voice_pipeline = VoicePipeline()
        await voice_pipeline.initialize()
        app.state.voice = voice_pipeline
    except Exception as e:
        logger.warning(f"Pipeline de voz no disponible: {e}. Sistema continúa sin voz.")
        app.state.voice = None

    # WebSocket manager
    app.state.ws_manager = ws_manager

    logger.info("✅ JARVIS-X listo. Escuchando en http://{}:{}".format(settings.HOST, settings.PORT))
    logger.info("Diga 'Jarvis' para activar el asistente.")

    yield

    # ── Shutdown ─────────────────────────────────────────────
    logger.info("Apagando JARVIS-X...")
    if voice_pipeline:
        await voice_pipeline.shutdown()
    if orchestrator:
        await orchestrator.shutdown()
    await close_cache()
    await close_db()
    logger.info("Sistema apagado correctamente.")


# ── Aplicación FastAPI ────────────────────────────────────────
app = FastAPI(
    title="JARVIS-X API",
    description="Sistema Operativo de IA Personal",
    version=settings.APP_VERSION,
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
    lifespan=lifespan,
)

# ── Middlewares ───────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(GZipMiddleware, minimum_size=1000)


@app.middleware("http")
async def add_process_time(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    elapsed = (time.perf_counter() - start) * 1000
    response.headers["X-Process-Time"] = f"{elapsed:.2f}ms"
    return response


@app.middleware("http")
async def security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    return response


# ── Routers ───────────────────────────────────────────────────
app.include_router(api_v1_router, prefix="/api/v1")
app.include_router(ws_router, prefix="/ws")

# Archivos estáticos (frontend compilado)
frontend_dist = Path("frontend/dist")
if frontend_dist.exists():
    app.mount("/", StaticFiles(directory=str(frontend_dist), html=True), name="frontend")


# ── Endpoints de sistema ──────────────────────────────────────
@app.get("/health", tags=["sistema"])
async def health_check():
    """Estado de salud del sistema."""
    return {
        "status": "operational",
        "version": settings.APP_VERSION,
        "name": "JARVIS-X",
        "subsystems": {
            "llm": llm_router.get_status() if llm_router else "offline",
            "memory": "online" if memory_manager else "offline",
            "agents": orchestrator.get_status() if orchestrator else "offline",
            "voice": "online" if voice_pipeline and voice_pipeline.is_ready else "offline",
        },
    }


@app.get("/", tags=["sistema"])
async def root():
    return {
        "message": "JARVIS-X, su asistente personal.",
        "version": settings.APP_VERSION,
        "docs": "/docs",
    }


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Error no controlado: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Error interno del sistema. JARVIS está trabajando en ello."},
    )


# ── Punto de entrada ─────────────────────────────────────────
if __name__ == "__main__":
    uvicorn.run(
        "backend.main:app",
        host=settings.HOST,
        port=settings.PORT,
        workers=1,  # 1 worker para WebSockets con estado compartido
        reload=settings.RELOAD,
        log_level=settings.LOG_LEVEL.lower(),
        access_log=settings.DEBUG,
        ws_ping_interval=20,
        ws_ping_timeout=10,
    )