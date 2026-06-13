from motor.motor_asyncio import AsyncIOMotorClient
import os
from typing import List, Dict, Any
from loguru import logger

class MongoDBConnector:
    def __init__(self):
        self.uri = os.getenv("MONGODB_URI", "mongodb://mongodb:27017")
        self.client = None
        self.db = None
        
    @classmethod
    def is_available(cls):
        return bool(os.getenv("MONGODB_URI"))
        
    async def connect(self):
        self.client = AsyncIOMotorClient(self.uri)
        self.db = self.client.jarvis
        logger.info("MongoDB connector initialized")
        
    async def insert_one(self, collection: str, document: Dict) -> str:
        result = await self.db[collection].insert_one(document)
        return str(result.inserted_id)
        
    async def find(self, collection: str, filter: Dict) -> List[Dict]:
        cursor = self.db[collection].find(filter)
        return await cursor.to_list(length=100)
        
    async def update_one(self, collection: str, filter: Dict, update: Dict) -> int:
        result = await self.db[collection].update_one(filter, {"$set": update})
        return result.modified_count
        
    async def disconnect(self):
        self.client.close()