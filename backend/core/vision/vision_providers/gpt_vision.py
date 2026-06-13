import base64
from openai import AsyncOpenAI
from PIL import Image
import io
from backend.config import settings

class GPTVision:
    @staticmethod
    async def analyze(image: Image.Image, prompt: str = "Describe esta imagen") -> str:
        client = AsyncOpenAI(api_key=settings.openai_api_key)
        buffered = io.BytesIO()
        image.save(buffered, format="PNG")
        img_base64 = base64.b64encode(buffered.getvalue()).decode()
        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{img_base64}"}}
                ]}
            ],
            max_tokens=500
        )
        return response.choices[0].message.content