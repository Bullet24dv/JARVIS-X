import os
from notion_client import AsyncClient
from typing import Dict, List, Any
from loguru import logger

class NotionConnector:
    def __init__(self):
        self.token = os.getenv("NOTION_API_KEY")
        self.client = None
        
    @classmethod
    def is_available(cls):
        return bool(os.getenv("NOTION_API_KEY"))
        
    async def connect(self):
        self.client = AsyncClient(auth=self.token)
        logger.info("Notion connector initialized")
        
    async def query_database(self, database_id: str, filter: Dict = None) -> List[Dict]:
        response = await self.client.databases.query(database_id=database_id, filter=filter)
        return response.get("results", [])
        
    async def create_page(self, parent_id: str, properties: Dict) -> Dict:
        return await self.client.pages.create(parent={"database_id": parent_id}, properties=properties)
        
    async def update_page(self, page_id: str, properties: Dict) -> Dict:
        return await self.client.pages.update(page_id=page_id, properties=properties)
        
    async def disconnect(self):
        await self.client.close()