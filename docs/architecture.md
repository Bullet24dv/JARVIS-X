# JARVIS-X Architecture

## High Level
- Backend: FastAPI + WebSockets + AsyncIO
- Frontend: PyQt6 + QML + WebEngine
- Database: PostgreSQL + MongoDB + ChromaDB
- Cache: Redis
- Message Broker: RabbitMQ
- LLM Router: Multi-provider with failover
- Agents: 10 specialized agents
- MCP: 15+ connectors
- Voice: Faster Whisper + Edge TTS / ElevenLabs
- Vision: OpenCV + EasyOCR + Gemini Vision
- Deployment: Docker Compose

## Flow
User -> Wake Word -> STT -> LLM Router -> Agent -> Action -> TTS -> User