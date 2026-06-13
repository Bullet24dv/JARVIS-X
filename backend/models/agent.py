from backend.models.database import db
from typing import Dict, List, Optional
from datetime import datetime

class Agent:
    collection = "agents"
    
    @staticmethod
    async def register(name: str, capabilities: List[str]) -> str:
        agent = {
            "name": name,
            "capabilities": capabilities,
            "status": "idle",
            "last_active": datetime.utcnow(),
            "created_at": datetime.utcnow()
        }
        result = await db[Agent.collection].insert_one(agent)
        return str(result.inserted_id)
        
    @staticmethod
    async def update_status(name: str, status: str):
        await db[Agent.collection].update_one(
            {"name": name},
            {"$set": {"status": status, "last_active": datetime.utcnow()}}
        )
        
    @staticmethod
    async def list_all() -> List[Dict]:
        cursor = db[Agent.collection].find({})
        return await cursor.to_list(length=100)