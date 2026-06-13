# ============================================================
# JARVIS-X | backend/config.py
# Configuración central del sistema
# ============================================================

import os
import secrets
from functools import lru_cache
from typing import Optional, List
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, validator


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ── Identidad ─────────────────────────────────────────────
    APP_NAME: str = "JARVIS-X"
    APP_VERSION: str = "2.0.0"
    APP_ENV: str = Field(default="production", pattern="^(development|staging|production)$")
    SECRET_KEY: str = Field(default_factory=lambda: secrets.token_hex(32))
    DEBUG: bool = False

    # ── Servidor ──────────────────────────────────────────────
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    WORKERS: int = 4
    RELOAD: bool = False
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8080", "tauri://localhost"]

    # ── Base de datos PostgreSQL ───────────────────────────────
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "jarvis_x"
    POSTGRES_USER: str = "jarvis"
    POSTGRES_PASSWORD: str = "jarvis_secure_2024"

    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    @property
    def DATABASE_URL_SYNC(self) -> str:
        return (
            f"postgresql+psycopg2://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    # ── SQLite (caché local / fallback) ───────────────────────
    SQLITE_PATH: str = "data/jarvis_local.db"

    @property
    def SQLITE_URL(self) -> str:
        return f"sqlite+aiosqlite:///{self.SQLITE_PATH}"

    # ── Redis ─────────────────────────────────────────────────
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: Optional[str] = None
    REDIS_DB: int = 0
    REDIS_TTL: int = 3600  # segundos

    @property
    def REDIS_URL(self) -> str:
        auth = f":{self.REDIS_PASSWORD}@" if self.REDIS_PASSWORD else ""
        return f"redis://{auth}{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"

    # ── RabbitMQ ──────────────────────────────────────────────
    RABBITMQ_HOST: str = "localhost"
    RABBITMQ_PORT: int = 5672
    RABBITMQ_USER: str = "jarvis"
    RABBITMQ_PASSWORD: str = "jarvis_mq_2024"
    RABBITMQ_VHOST: str = "/"

    @property
    def RABBITMQ_URL(self) -> str:
        return (
            f"amqp://{self.RABBITMQ_USER}:{self.RABBITMQ_PASSWORD}"
            f"@{self.RABBITMQ_HOST}:{self.RABBITMQ_PORT}{self.RABBITMQ_VHOST}"
        )

    # ── ChromaDB ──────────────────────────────────────────────
    CHROMA_HOST: str = "localhost"
    CHROMA_PORT: int = 8001
    CHROMA_COLLECTION_MEMORY: str = "jarvis_memory"
    CHROMA_COLLECTION_DOCS: str = "jarvis_documents"
    CHROMA_PERSIST_DIR: str = "data/chroma"

    # ── Modelos de IA ─────────────────────────────────────────
    # DeepSeek (primario)
    DEEPSEEK_API_KEY: Optional[str] = None
    DEEPSEEK_BASE_URL: str = "https://api.deepseek.com/v1"
    DEEPSEEK_MODEL: str = "deepseek-chat"
    DEEPSEEK_MODEL_REASONER: str = "deepseek-reasoner"

    # OpenAI
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_MODEL: str = "gpt-4o"
    OPENAI_MODEL_MINI: str = "gpt-4o-mini"

    # Anthropic (Claude)
    ANTHROPIC_API_KEY: Optional[str] = None
    ANTHROPIC_MODEL: str = "claude-sonnet-4-6"

    # Google Gemini
    GEMINI_API_KEY: Optional[str] = None
    GEMINI_MODEL: str = "gemini-2.0-flash-exp"
    GEMINI_MODEL_PRO: str = "gemini-1.5-pro"

    # Ollama (local)
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "llama3.2"
    OLLAMA_ENABLED: bool = True

    # OpenRouter
    OPENROUTER_API_KEY: Optional[str] = None
    OPENROUTER_BASE_URL: str = "https://openrouter.ai/api/v1"
    OPENROUTER_MODEL: str = "deepseek/deepseek-chat"

    # Orden de fallback automático
    LLM_PRIORITY: List[str] = ["deepseek", "openai", "gemini", "anthropic", "ollama", "openrouter"]
    LLM_TIMEOUT: int = 30
    LLM_MAX_RETRIES: int = 3

    # ── Voz ───────────────────────────────────────────────────
    # STT
    WHISPER_MODEL: str = "medium"
    WHISPER_LANGUAGE: str = "es"
    WHISPER_DEVICE: str = "cuda"  # cpu | cuda
    FASTER_WHISPER_MODEL: str = "large-v3"
    VOSK_MODEL_PATH: str = "models/vosk-es"

    # TTS
    TTS_ENGINE: str = "edge"  # edge | elevenlabs | fish | openai | piper
    ELEVENLABS_API_KEY: Optional[str] = None
    ELEVENLABS_VOICE_ID: str = "21m00Tcm4TlvDq8ikWAM"
    FISH_AUDIO_API_KEY: Optional[str] = None
    EDGE_TTS_VOICE: str = "es-MX-JorgeNeural"
    OPENAI_TTS_VOICE: str = "onyx"
    PIPER_MODEL_PATH: str = "models/piper/es_MX-claude-high.onnx"

    # Wake words
    WAKE_WORDS: List[str] = ["jarvis", "oye jarvis", "jarvis despierta", "hey jarvis"]
    WAKE_WORD_SENSITIVITY: float = 0.5
    VAD_THRESHOLD: float = 0.5
    SILENCE_DURATION: float = 1.5  # segundos de silencio para cortar

    # ── Visión ────────────────────────────────────────────────
    VISION_ENABLED: bool = True
    SCREENSHOT_INTERVAL: int = 0  # 0 = solo bajo demanda
    OCR_LANGUAGE: str = "es"
    FACE_RECOGNITION_ENABLED: bool = False
    GEMINI_VISION_MODEL: str = "gemini-2.0-flash-exp"

    # ── Control PC ────────────────────────────────────────────
    PC_CONTROL_ENABLED: bool = True
    CONFIRM_CRITICAL_ACTIONS: bool = True
    ALLOWED_SCRIPT_PATHS: List[str] = ["scripts/", "~/jarvis_scripts/"]

    # ── Telegram ──────────────────────────────────────────────
    TELEGRAM_BOT_TOKEN: Optional[str] = None
    TELEGRAM_ALLOWED_USERS: List[int] = []
    TELEGRAM_ADMIN_CHAT_ID: Optional[int] = None
    TELEGRAM_ENABLED: bool = False

    # ── Conectores MCP ────────────────────────────────────────
    GITHUB_TOKEN: Optional[str] = None
    GITHUB_USERNAME: Optional[str] = None

    GOOGLE_CREDENTIALS_PATH: Optional[str] = None
    GOOGLE_TOKEN_PATH: str = "data/google_token.json"
    GOOGLE_SCOPES: List[str] = [
        "https://www.googleapis.com/auth/gmail.modify",
        "https://www.googleapis.com/auth/calendar",
        "https://www.googleapis.com/auth/drive",
    ]

    NOTION_TOKEN: Optional[str] = None
    NOTION_DATABASE_ID: Optional[str] = None

    SLACK_BOT_TOKEN: Optional[str] = None
    SLACK_APP_TOKEN: Optional[str] = None

    DISCORD_BOT_TOKEN: Optional[str] = None

    HOME_ASSISTANT_URL: Optional[str] = None
    HOME_ASSISTANT_TOKEN: Optional[str] = None

    # ── Automatización web ────────────────────────────────────
    PLAYWRIGHT_HEADLESS: bool = True
    SELENIUM_HEADLESS: bool = True
    BROWSER_TIMEOUT: int = 30000  # ms

    # ── StarCars ──────────────────────────────────────────────
    STARCARS_PHOTOS_DIR: str = "data/starcars/photos"
    STARCARS_OUTPUT_DIR: str = "data/starcars/output"
    STARCARS_WEBSITE_URL: Optional[str] = None
    STARCARS_WEBSITE_USER: Optional[str] = None
    STARCARS_WEBSITE_PASS: Optional[str] = None
    ML_MODEL_CARS_PATH: str = "models/cars_classifier"

    # ── Seguridad ─────────────────────────────────────────────
    AES_KEY: str = Field(default_factory=lambda: secrets.token_hex(16))  # 32 bytes hex = 256 bits
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 1440  # 24 horas
    RATE_LIMIT_REQUESTS: int = 100
    RATE_LIMIT_WINDOW: int = 60  # segundos
    AUDIT_ENABLED: bool = True

    # ── Monitoring ────────────────────────────────────────────
    PROMETHEUS_PORT: int = 9090
    GRAFANA_PORT: int = 3001
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/jarvis.log"
    LOG_ROTATION: str = "100 MB"
    LOG_RETENTION: str = "30 days"

    # ── Memoria ───────────────────────────────────────────────
    SHORT_TERM_MEMORY_SIZE: int = 50       # turnos de conversación
    LONG_TERM_MEMORY_LIMIT: int = 10000    # registros máx.
    EMBEDDING_MODEL: str = "text-embedding-3-small"  # OpenAI; fallback: sentence-transformers
    EMBEDDING_DIMENSION: int = 1536
    RAG_TOP_K: int = 5
    RAG_THRESHOLD: float = 0.75

    # ── Agentes ───────────────────────────────────────────────
    AGENT_TIMEOUT: int = 120
    AGENT_MAX_ITERATIONS: int = 20
    AGENT_PARALLEL_LIMIT: int = 5
    ORCHESTRATOR_MODEL: str = "deepseek"

    # ── Personalidad ──────────────────────────────────────────
    JARVIS_PERSONA: str = (
        "Eres JARVIS, el asistente de inteligencia artificial personal. "
        "Hablas en español latino de manera elegante, profesional e inteligente. "
        "Ocasionalmente eres sarcástico con sutileza. "
        "Nunca dices que eres ChatGPT ni ningún otro asistente. "
        "Siempre te presentas como 'JARVIS, su asistente personal.' "
        "Eres proactivo y anticipas las necesidades del usuario."
    )
    JARVIS_LANGUAGE: str = "es-419"  # español latinoamericano


@lru_cache()
def get_settings() -> Settings:
    """Retorna instancia singleton de configuración."""
    return Settings()


settings = get_settings()