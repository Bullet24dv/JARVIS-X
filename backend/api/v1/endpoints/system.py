from fastapi import APIRouter, HTTPException
import psutil
import platform
from datetime import datetime

router = APIRouter()

@router.get("/status")
async def system_status():
    return {
        "os": platform.system(),
        "os_version": platform.version(),
        "python_version": platform.python_version(),
        "cpu_percent": psutil.cpu_percent(interval=1),
        "memory_percent": psutil.virtual_memory().percent,
        "disk_usage": psutil.disk_usage('/').percent,
        "uptime": datetime.now().isoformat()
    }

@router.post("/restart")
async def restart_service():
    # Implementar reinicio controlado
    return {"status": "restarting"}