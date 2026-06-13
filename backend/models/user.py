from backend.models.database import db
from bson import ObjectId
from typing import Optional, Dict
from datetime import datetime

class User:
    collection = "users"
    
    @staticmethod
    async def create(data: dict) -> str:
        data["created_at"] = datetime.utcnow()
        data["updated_at"] = datetime.utcnow()
        result = await db[User.collection].insert_one(data)
        return str(result.inserted_id)
        
    @staticmethod
    async def find_one(filter: dict) -> Optional[Dict]:
        return await db[User.collection].find_one(filter)
        
    @staticmethod
    async def find_by_id(user_id: str) -> Optional[Dict]:
        return await db[User.collection].find_one({"_id": ObjectId(user_id)})
        
    @staticmethod
    async def update(user_id: str, data: dict) -> bool:
        data["updated_at"] = datetime.utcnow()
        result = await db[User.collection].update_one(
            {"_id": ObjectId(user_id)},
            {"$set": data}
        )
        return result.modified_count > 0
        
    @staticmethod
    async def delete(user_id: str) -> bool:
        result = await db[User.collection].delete_one({"_id": ObjectId(user_id)})
        return result.deleted_count > 0