import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

if __name__ == "__main__":
    requirements = [
        "fastapi", "uvicorn", "websockets", "aiohttp", "pydantic",
        "sqlalchemy", "asyncpg", "chromadb", "redis", "aio-pika",
        "openai", "google-generativeai", "anthropic", "ollama",
        "faster-whisper", "vosk", "elevenlabs", "edge-tts", "pyautogui",
        "opencv-python", "easyocr", "pytesseract", "pillow",
        "PyQt6", "PyQt6-WebEngine", "slack-sdk", "discord.py",
        "motor", "aiomysql", "schedule", "loguru", "python-dotenv"
    ]
    for pkg in requirements:
        print(f"Installing {pkg}...")
        install(pkg)