from backend.core.mcp.mcp_server import MCPServer
from typing import Dict, Any
from loguru import logger

class MCPService:
    def __init__(self):
        self.server = MCPServer()
        
    async def connect_all(self):
        await self.server.connect_all()
        
    async def disconnect_all(self):
        await self.server.disconnect_all()
        
    async def execute_tool(self, tool_name: str, params: Dict) -> Any:
        return await self.server.execute_tool(tool_name, params)
        
    async def list_connectors(self) -> list:
        return list(self.server.connectors.keys())