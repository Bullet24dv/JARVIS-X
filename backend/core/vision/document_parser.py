from pypdf import PdfReader
from docx import Document
import pandas as pd
from PIL import Image
from backend.core.vision.ocr_engine import OCREngine

class DocumentParser:
    def __init__(self):
        self.ocr = OCREngine()
        
    async def parse_pdf(self, file_path: str) -> str:
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text
        
    async def parse_docx(self, file_path: str) -> str:
        doc = Document(file_path)
        text = "\n".join([para.text for para in doc.paragraphs])
        return text
        
    async def parse_excel(self, file_path: str) -> dict:
        df = pd.read_excel(file_path)
        return df.to_dict(orient="records")
        
    async def parse_image(self, image: Image.Image) -> str:
        return await self.ocr.extract_text(image)