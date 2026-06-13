import aiohttp
import json
from typing import Dict, Any
from loguru import logger

class MCPClient:
    def __init__(self, server_url: str):
        self.server_url = server_url
        self.session = None
        
    async def connect(self):
        self.session = aiohttp.ClientSession()
        logger.info(f"MCP Client connected to {self.server_url}")
        
    async def call_tool(self, tool_name: str, params: Dict[str, Any]) -> Any:
        async with self.session.post(f"{self.server_url}/call", json={"tool": tool_name, "params": params}) as resp:
            return await resp.json()
            
    async def list_tools(self) -> list:
        async with self.session.get(f"{self.server_url}/tools") as resp:
            return await resp.json()
            
    async def disconnect(self):
        if self.session:
            await self.session.close()