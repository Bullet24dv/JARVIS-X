import easyocr
import cv2
import numpy as np
from PIL import Image
from loguru import logger

class OCREngine:
    def __init__(self, languages: list = None):
        self.languages = languages or ['es', 'en']
        self.reader = None
        
    async def initialize(self):
        self.reader = easyocr.Reader(self.languages, gpu=False)
        logger.info("OCR Engine initialized")
        
    async def extract_text(self, image: Image.Image) -> str:
        img_np = np.array(image)
        results = self.reader.readtext(img_np, detail=0, paragraph=True)
        return " ".join(results)
        
    async def extract_license_plate(self, image: Image.Image) -> str:
        img_np = np.array(image)
        gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)
        # Preprocessing específico para patentes
        gray = cv2.bilateralFilter(gray, 9, 75, 75)
        results = self.reader.readtext(gray, detail=0, allowlist="ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
        for text in results:
            if len(text) >= 5 and any(c.isdigit() for c in text):
                return text
        return ""
        
    async def extract_text_boxes(self, image: Image.Image) -> list:
        img_np = np.array(image)
        results = self.reader.readtext(img_np, detail=1)
        return [{"text": res[1], "confidence": res[2], "bbox": res[0]} for res in results]