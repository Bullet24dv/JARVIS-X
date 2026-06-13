import os
import aiohttp
from typing import Dict, Any, List
from loguru import logger

class HomeAssistantConnector:
    def __init__(self):
        self.url = os.getenv("HOME_ASSISTANT_URL", "http://localhost:8123")
        self.token = os.getenv("HOME_ASSISTANT_TOKEN")
        self.session = None
        
    @classmethod
    def is_available(cls):
        return bool(os.getenv("HOME_ASSISTANT_TOKEN"))
        
    async def connect(self):
        self.session = aiohttp.ClientSession()
        logger.info("Home Assistant connector initialized")
        
    async def get_states(self) -> List[Dict]:
        async with self.session.get(f"{self.url}/api/states", headers={"Authorization": f"Bearer {self.token}"}) as resp:
            return await resp.json()
            
    async def turn_on(self, entity_id: str) -> Dict:
        async with self.session.post(f"{self.url}/api/services/light/turn_on", json={"entity_id": entity_id}, headers={"Authorization": f"Bearer {self.token}"}) as resp:
            return await resp.json()
            
    async def turn_off(self, entity_id: str) -> Dict:
        async with self.session.post(f"{self.url}/api/services/light/turn_off", json={"entity_id": entity_id}, headers={"Authorization": f"Bearer {self.token}"}) as resp:
            return await resp.json()
            
    async def get_entity_state(self, entity_id: str) -> Dict:
        async with self.session.get(f"{self.url}/api/states/{entity_id}", headers={"Authorization": f"Bearer {self.token}"}) as resp:
            return await resp.json()
            
    async def disconnect(self):
        await self.session.close()