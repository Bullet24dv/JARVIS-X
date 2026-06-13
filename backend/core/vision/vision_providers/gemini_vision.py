import google.generativeai as genai
from PIL import Image
from backend.config import settings

class GeminiVision:
    @staticmethod
    async def analyze(image: Image.Image, prompt: str = "Describe esta imagen") -> str:
        genai.configure(api_key=settings.gemini_api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content([prompt, image])
        return response.text