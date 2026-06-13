"""
ElevenLabs TTS Provider for JARVIS-X
Síntesis de voz con calidad profesional usando ElevenLabs API
"""

import aiohttp
import asyncio
import base64
from typing import Optional, Dict, Any
from loguru import logger
from backend.config import settings


class ElevenLabsTTS:
    """Proveedor de Text-to-Speech usando ElevenLabs API"""
    
    def __init__(self):
        self.api_key = settings.elevenlabs_api_key
        self.voice_id = settings.elevenlabs_voice_id
        self.base_url = "https://api.elevenlabs.io/v1"
        self.session: Optional[aiohttp.ClientSession] = None
        self.available = False
        
    async def initialize(self) -> bool:
        """Inicializa el cliente de ElevenLabs"""
        if not self.api_key:
            logger.warning("ElevenLabs API key not configured. Voice synthesis will not work.")
            return False
        
        self.session = aiohttp.ClientSession()
        self.available = True
        logger.info(f"ElevenLabs TTS initialized with voice ID: {self.voice_id}")
        return True
    
    async def _request(self, endpoint: str, method: str = "GET", data: Optional[Dict] = None) -> Dict:
        """Realiza una petición a la API de ElevenLabs"""
        headers = {
            "xi-api-key": self.api_key,
            "Content-Type": "application/json"
        }
        
        url = f"{self.base_url}{endpoint}"
        
        async with self.session.request(method, url, headers=headers, json=data) as response:
            if response.status != 200:
                error_text = await response.text()
                logger.error(f"ElevenLabs API error {response.status}: {error_text}")
                raise Exception(f"ElevenLabs API error: {response.status}")
            return await response.json()
    
    async def get_voices(self) -> list:
        """Obtiene la lista de voces disponibles"""
        if not self.available:
            return []
        
        result = await self._request("/voices")
        return result.get("voices", [])
    
    async def synthesize(
        self, 
        text: str, 
        voice_id: Optional[str] = None,
        stability: float = 0.5,
        similarity_boost: float = 0.75,
        style: float = 0.0,
        use_speaker_boost: bool = True
    ) -> bytes:
        """
        Sintetiza texto a voz usando ElevenLabs
        
        Args:
            text: Texto a sintetizar (máximo 5000 caracteres)
            voice_id: ID de la voz a usar (opcional, usa la configurada por defecto)
            stability: Estabilidad de la voz (0.0 - 1.0)
            similarity_boost: Similitud con la voz original (0.0 - 1.0)
            style: Estilo de la voz (0.0 - 1.0)
            use_speaker_boost: Mejora del altavoz
        
        Returns:
            bytes: Audio en formato MP3
        """
        if not self.available:
            raise Exception("ElevenLabs TTS not initialized. Check API key.")
        
        if not text or len(text) > 5000:
            raise ValueError("Text must be between 1 and 5000 characters")
        
        voice = voice_id or self.voice_id
        
        headers = {
            "xi-api-key": self.api_key,
            "Content-Type": "application/json"
        }
        
        data = {
            "text": text,
            "voice_settings": {
                "stability": stability,
                "similarity_boost": similarity_boost,
                "style": style,
                "use_speaker_boost": use_speaker_boost
            }
        }
        
        url = f"{self.base_url}/text-to-speech/{voice}"
        
        async with self.session.post(url, headers=headers, json=data) as response:
            if response.status != 200:
                error_text = await response.text()
                logger.error(f"ElevenLabs synthesis error: {error_text}")
                raise Exception(f"Failed to synthesize: {response.status}")
            
            audio_data = await response.read()
            logger.info(f"Synthesized {len(text)} chars to {len(audio_data)} bytes")
            return audio_data
    
    async def synthesize_stream(
        self,
        text: str,
        voice_id: Optional[str] = None,
        stability: float = 0.5,
        similarity_boost: float = 0.75
    ) -> aiohttp.ClientResponse:
        """
        Sintetiza texto a voz en modo streaming (para respuestas largas)
        
        Args:
            text: Texto a sintetizar
            voice_id: ID de la voz a usar
            stability: Estabilidad de la voz
            similarity_boost: Similitud con la voz original
        
        Returns:
            ClientResponse: Stream de audio en formato MP3
        """
        if not self.available:
            raise Exception("ElevenLabs TTS not initialized")
        
        voice = voice_id or self.voice_id
        
        headers = {
            "xi-api-key": self.api_key,
            "Content-Type": "application/json"
        }
        
        data = {
            "text": text,
            "voice_settings": {
                "stability": stability,
                "similarity_boost": similarity_boost
            }
        }
        
        url = f"{self.base_url}/text-to-speech/{voice}/stream"
        
        response = await self.session.post(url, headers=headers, json=data)
        
        if response.status != 200:
            error_text = await response.text()
            raise Exception(f"Failed to stream synthesis: {response.status} - {error_text}")
        
        return response
    
    async def get_voice_settings(self, voice_id: Optional[str] = None) -> Dict:
        """Obtiene la configuración de una voz específica"""
        if not self.available:
            return {}
        
        voice = voice_id or self.voice_id
        result = await self._request(f"/voices/{voice}/settings")
        return result
    
    async def close(self):
        """Cierra la sesión HTTP"""
        if self.session:
            await self.session.close()
            self.available = False
    
    async def __aenter__(self):
        await self.initialize()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()


# Función de conveniencia para uso rápido
async def quick_synthesize(text: str, voice_id: Optional[str] = None) -> bytes:
    """
    Función rápida para sintetizar texto a voz
    
    Ejemplo:
        audio = await quick_synthesize("Hola, soy JARVIS")
        with open("output.mp3", "wb") as f:
            f.write(audio)
    """
    async with ElevenLabsTTS() as tts:
        return await tts.synthesize(text, voice_id)


# Lista de voces en español recomendadas
RECOMMENDED_SPANISH_VOICES = {
    "latino_masculino": "21m00Tcm4TlvDq8ikWAM",  # Adam - voz masculina neutra
    "latino_femenino": "AZnzlk1XvdvUeBnXmlld",   # Bella - voz femenina
    "españa_masculino": "EXAVITQu4L4MjXvX3hKz", # Josh - voz española
    "españa_femenino": "Xp1hP8pZz4t3YjK9qR2w",  # Nicole - voz española
}