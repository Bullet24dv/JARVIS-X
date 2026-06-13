import cv2
import face_recognition
from PIL import Image
import numpy as np
from loguru import logger

class FaceRecognizer:
    def __init__(self):
        self.known_face_encodings = []
        self.known_face_names = []
        
    async def add_known_face(self, image: Image.Image, name: str):
        img_np = np.array(image)
        encodings = face_recognition.face_encodings(img_np)
        if encodings:
            self.known_face_encodings.append(encodings[0])
            self.known_face_names.append(name)
            logger.info(f"Added face for {name}")
            
    async def recognize_faces(self, image: Image.Image) -> list:
        img_np = np.array(image)
        face_locations = face_recognition.face_locations(img_np)
        face_encodings = face_recognition.face_encodings(img_np, face_locations)
        recognized = []
        for encoding in face_encodings:
            matches = face_recognition.compare_faces(self.known_face_encodings, encoding)
            name = "Desconocido"
            if True in matches:
                first_match_index = matches.index(True)
                name = self.known_face_names[first_match_index]
            recognized.append({"name": name, "location": face_locations[0]})
        return recognized