import cv2
from deepface import DeepFace
from PIL import Image
import numpy as np
from loguru import logger

class EmotionRecognizer:
    async def detect_emotion(self, image: Image.Image) -> dict:
        img_np = np.array(image)
        try:
            result = DeepFace.analyze(img_np, actions=['emotion'], enforce_detection=False)
            return result[0]['emotion']
        except Exception as e:
            logger.error(f"Emotion detection failed: {e}")
            return {"neutral": 0.8}