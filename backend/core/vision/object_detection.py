import cv2
import numpy as np
from PIL import Image
import torch
from transformers import AutoModelForObjectDetection, AutoImageProcessor
from loguru import logger

class ObjectDetector:
    def __init__(self):
        self.model_name = "facebook/detr-resnet-50"
        self.processor = None
        self.model = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
    async def initialize(self):
        self.processor = AutoImageProcessor.from_pretrained(self.model_name)
        self.model = AutoModelForObjectDetection.from_pretrained(self.model_name).to(self.device)
        logger.info(f"Object detector initialized on {self.device}")
        
    async def detect_objects(self, image: Image.Image, threshold: float = 0.5) -> list:
        inputs = self.processor(images=image, return_tensors="pt").to(self.device)
        with torch.no_grad():
            outputs = self.model(**inputs)
        target_sizes = torch.tensor([image.size[::-1]]).to(self.device)
        results = self.processor.post_process_object_detection(outputs, threshold=threshold, target_sizes=target_sizes)[0]
        objects = []
        for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
            objects.append({
                "label": self.model.config.id2label[label.item()],
                "confidence": score.item(),
                "box": box.tolist()
            })
        return objects
        
    async def detect_brand(self, image: Image.Image) -> dict:
        # Placeholder para demo - en producción usar modelo fine-tuned
        objects = await self.detect_objects(image, threshold=0.6)
        # Simulación de detección de auto
        car_labels = ["car", "truck", "bus"]
        for obj in objects:
            if obj["label"] in car_labels:
                return {"brand": "Toyota", "model": "Corolla", "confidence": 0.85}
        return {"brand": None, "model": None, "confidence": 0}