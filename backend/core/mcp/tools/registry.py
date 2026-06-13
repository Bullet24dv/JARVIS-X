from typing import Dict, Any, Callable
from loguru import logger

class MCPToolRegistry:
    def __init__(self):
        self.tools: Dict[str, Callable] = {}
        
    def register(self, name: str, func: Callable):
        self.tools[name] = func
        logger.debug(f"Registered MCP tool: {name}")
        
    def get(self, name: str) -> Callable:
        return self.tools.get(name)
        
    def list_tools(self) -> list:
        return list(self.tools.keys())
        
    async def execute(self, name: str, params: Dict[str, Any]) -> Any:
        tool = self.get(name)
        if not tool:
            raise ValueError(f"Tool {name} not found")
        return await tool(**params)

mcp_tool_registry = MCPToolRegistry()