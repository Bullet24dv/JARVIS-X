from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.services.computer_service import ComputerService
import platform

router = APIRouter()
computer_service = ComputerService()

class AppRequest(BaseModel):
    name: str

class ScriptRequest(BaseModel):
    path: str

@router.post("/open")
async def open_app(request: AppRequest):
    result = await computer_service.open_app(request.name)
    if not result:
        raise HTTPException(status_code=400, detail="Could not open app")
    return {"status": "opened", "app": request.name}

@router.post("/close")
async def close_app(request: AppRequest):
    result = await computer_service.close_app(request.name)
    return {"status": "closed" if result else "not found"}

@router.get("/running")
async def list_running():
    apps = await computer_service.list_running()
    return {"apps": apps}

@router.post("/script")
async def run_script(request: ScriptRequest):
    output = await computer_service.execute_script(request.path)
    return {"output": output}

@router.post("/mouse/click")
async def mouse_click(x: int = None, y: int = None, button: str = "left"):
    await computer_service.mouse_click(x, y, button)
    return {"status": "clicked"}

@router.post("/keyboard/type")
async def type_text(text: str):
    await computer_service.type_text(text)
    return {"status": "typed"}