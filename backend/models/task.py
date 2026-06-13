from backend.models.database import db
from bson import ObjectId
from typing import Dict, List, Optional
from datetime import datetime
from enum import Enum

class TaskStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"

class Task:
    collection = "tasks"
    
    @staticmethod
    async def create(task_data: dict) -> str:
        task_data["created_at"] = datetime.utcnow()
        task_data["updated_at"] = datetime.utcnow()
        task_data["status"] = TaskStatus.PENDING
        result = await db[Task.collection].insert_one(task_data)
        return str(result.inserted_id)
        
    @staticmethod
    async def update_status(task_id: str, status: TaskStatus, result: dict = None):
        update = {"status": status, "updated_at": datetime.utcnow()}
        if result:
            update["result"] = result
        await db[Task.collection].update_one(
            {"_id": ObjectId(task_id)},
            {"$set": update}
        )
        
    @staticmethod
    async def get_pending() -> List[Dict]:
        cursor = db[Task.collection].find({"status": TaskStatus.PENDING}).sort("created_at", 1)
        return await cursor.to_list(length=100)