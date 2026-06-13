from .base_agent import BaseAgent
from typing import Dict, Any

class SmartHomeAgent(BaseAgent):
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        action = input_data.get("action")
        if action == "control_device":
            return await self.control_device(input_data["device"], input_data["command"])
        elif action == "get_status":
            return await self.house_status()
        return {"error": "Unknown action"}
        
    async def control_device(self, device: str, command: str) -> Dict:
        # Integración con Home Assistant vía MCP
        from backend.core.mcp.connectors.homeassistant import HomeAssistantConnector
        ha = HomeAssistantConnector()
        await ha.connect()
        if command == "on":
            await ha.turn_on(device)
        elif command == "off":
            await ha.turn_off(device)
        await ha.disconnect()
        return {"device": device, "command": command, "status": "executed"}
        
    async def house_status(self) -> Dict:
        # Mock
        return {"lights": "off", "temperature": 22, "security": "armed"}