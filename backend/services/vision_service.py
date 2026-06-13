from backend.core.vision.screen_capture import ScreenCapture
from backend.core.vision.ocr_engine import OCREngine
from backend.core.vision.object_detection import ObjectDetector
from backend.core.vision.document_parser import DocumentParser
from PIL import Image
from loguru import logger

class VisionService:
    def __init__(self):
        self.capture = ScreenCapture()
        self.ocr = OCREngine()
        self.detector = ObjectDetector()
        self.parser = DocumentParser()
        
    async def initialize(self):
        await self.ocr.initialize()
        await self.detector.initialize()
        
    async def capture_screen(self) -> Image.Image:
        return await self.capture.capture_fullscreen()
        
    async def extract_text(self, image: Image.Image) -> str:
        return await self.ocr.extract_text(image)
        
    async def detect_objects(self, image: Image.Image) -> list:
        return await self.detector.detect_objects(image)
        
    async def parse_document(self, file_path: str) -> str:
        if file_path.endswith('.pdf'):
            return await self.parser.parse_pdf(file_path)
        elif file_path.endswith('.docx'):
            return await self.parser.parse_docx(file_path)
        elif file_path.endswith(('.xlsx', '.xls')):
            return await self.parser.parse_excel(file_path)
        else:
            return "Formato no soportado"