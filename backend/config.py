from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    # DeepSeek
    deepseek_api_key: str
    deepseek_base_url: str = "https://api.deepseek.com"
    
    # Other LLMs
    openai_api_key: Optional[str] = None
    gemini_api_key: Optional[str] = None
    claude_api_key: Optional[str] = None
    ollama_host: str = "http://localhost:11434"
    
    # Voice
    elevenlabs_api_key: Optional[str] = None
    elevenlabs_voice_id: str = "21m00Tcm4TlvDq8ikWAM"
    fish_audio_api_key: Optional[str] = None
    edge_tts_voice: str = "es-CL-CatalinaNeural"
    jarvis_voice: str = "edge_tts"
    jarvis_language: str = "es-LA"
    jarvis_wake_words: str = "jarvis,oye jarvis"
    jarvis_stt_engine: str = "faster_whisper"
    jarvis_tts_rate: float = 1.0          # <--- DEFINIDO
    
    # Telegram
    telegram_bot_token: Optional[str] = None
    
    # GitHub
    github_token: Optional[str] = None
    
    # Notion
    notion_api_key: Optional[str] = None
    
    # Slack
    slack_bot_token: Optional[str] = None
    slack_app_token: Optional[str] = None
    
    # Discord
    discord_bot_token: Optional[str] = None
    
    # Google
    google_client_id: Optional[str] = None
    google_client_secret: Optional[str] = None
    
    # Home Assistant
    home_assistant_url: Optional[str] = None
    home_assistant_token: Optional[str] = None
    
    # Database (PostgreSQL)
    postgres_user: str = "jarvis"          # <--- DEFINIDO
    postgres_password: str = "securepassword"  # <--- DEFINIDO
    postgres_db: str = "jarvis"            # <--- DEFINIDO
    database_url: str = "postgresql://jarvis:securepassword@localhost:5432/jarvis"
    redis_url: str = "redis://localhost:6379"
    redis_password: Optional[str] = None
    rabbitmq_url: str = "amqp://guest:guest@localhost:5672"
    mongodb_uri: str = "mongodb://localhost:27017"
    mysql_host: str = "localhost"
    mysql_port: int = 3306
    mysql_user: str = "jarvis"
    mysql_password: str = ""
    mysql_db: str = "jarvis"
    
    # Security
    secret_key: str
    encryption_key: str
    
    # Paths
    jarvis_temp_dir: str = "/tmp/jarvis"
    log_level: str = "INFO"
    log_file: str = "logs/jarvis.log"
    
    # Performance
    max_workers: int = 4
    async_workers: int = 8
    cache_ttl: int = 3600
    
    # Permite campos extra del .env sin error
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()