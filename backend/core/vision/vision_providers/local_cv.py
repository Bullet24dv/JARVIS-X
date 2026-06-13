import cv2
import numpy as np
from PIL import Image

class LocalCV:
    @staticmethod
    async def detect_edges(image: Image.Image) -> Image.Image:
        img_np = np.array(image.convert("L"))
        edges = cv2.Canny(img_np, 100, 200)
        return Image.fromarray(edges)
        
    @staticmethod
    async def detect_contours(image: Image.Image) -> list:
        img_np = np.array(image.convert("L"))
        _, thresh = cv2.threshold(img_np, 127, 255, 0)
        contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        return [c.tolist() for c in contours]