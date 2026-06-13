from backend.models.database import db
from bson import ObjectId
from typing import List, Dict
from datetime import datetime

class Memory:
    collection = "memories"
    
    @staticmethod
    async def store(user_id: str, text: str, memory_type: str, metadata: dict = None):
        memory = {
            "user_id": user_id,
            "text": text,
            "memory_type": memory_type,
            "metadata": metadata or {},
            "timestamp": datetime.utcnow(),
            "access_count": 0
        }
        result = await db[Memory.collection].insert_one(memory)
        return str(result.inserted_id)
        
    @staticmethod
    async def retrieve(user_id: str, memory_type: str = None, limit: int = 100) -> List[Dict]:
        filter = {"user_id": user_id}
        if memory_type:
            filter["memory_type"] = memory_type
        cursor = db[Memory.collection].find(filter).sort("timestamp", -1).limit(limit)
        return await cursor.to_list(length=limit)
        
    @staticmethod
    async def increment_access(memory_id: str):
        await db[Memory.collection].update_one(
            {"_id": ObjectId(memory_id)},
            {"$inc": {"access_count": 1}}
        )