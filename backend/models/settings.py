from backend.models.database import db
from typing import Dict, Any
from datetime import datetime

class Settings:
    collection = "settings"
    
    @staticmethod
    async def get(key: str) -> Any:
        doc = await db[Settings.collection].find_one({"_id": key})
        return doc.get("value") if doc else None
        
    @staticmethod
    async def set(key: str, value: Any):
        await db[Settings.collection].update_one(
            {"_id": key},
            {"$set": {"value": value, "updated_at": datetime.utcnow()}},
            upsert=True
        )