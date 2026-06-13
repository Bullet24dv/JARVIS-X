from backend.models.database import db
from bson import ObjectId
from typing import List, Dict
from datetime import datetime

class Conversation:
    collection = "conversations"
    
    @staticmethod
    async def add_message(user_id: str, role: str, content: str, metadata: dict = None):
        message = {
            "user_id": user_id,
            "role": role,
            "content": content,
            "timestamp": datetime.utcnow(),
            "metadata": metadata or {}
        }
        result = await db[Conversation.collection].insert_one(message)
        return str(result.inserted_id)
        
    @staticmethod
    async def get_history(user_id: str, limit: int = 50) -> List[Dict]:
        cursor = db[Conversation.collection].find({"user_id": user_id}).sort("timestamp", -1).limit(limit)
        return await cursor.to_list(length=limit)
        
    @staticmethod
    async def delete_old(older_than_days: int = 30):
        cutoff = datetime.utcnow() - datetime.timedelta(days=older_than_days)
        result = await db[Conversation.collection].delete_many({"timestamp": {"$lt": cutoff}})
        return result.deleted_count