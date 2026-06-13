from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel
from backend.services.vision_service import VisionService
from PIL import Image
import io

router = APIRouter()

@router.post("/ocr")
async def ocr_image(file: UploadFile = File(...)):
    vision = VisionService()
    contents = await file.read()
    image = Image.open(io.BytesIO(contents))
    text = await vision.extract_text(image)
    return {"text": text}

@router.post("/detect-objects")
async def detect_objects(file: UploadFile = File(...)):
    vision = VisionService()
    contents = await file.read()
    image = Image.open(io.BytesIO(contents))
    objects = await vision.detect_objects(image)
    return {"objects": objects}

@router.get("/screenshot")
async def screenshot():
    vision = VisionService()
    screenshot = await vision.capture_screen()
    # Convertir a base64
    import base64
    buffered = io.BytesIO()
    screenshot.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return {"screenshot": img_str}