import psutil
from .base_agent import BaseAgent
from typing import Dict, Any

class SecurityAgent(BaseAgent):
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        action = input_data.get("action")
        if action == "audit":
            return await self.audit_system()
        elif action == "monitor":
            return await self.get_threats()
        return {"error": "Unknown action"}
        
    async def audit_system(self) -> Dict:
        # Revisar procesos, puertos abiertos, etc.
        open_ports = []
        for conn in psutil.net_connections():
            if conn.status == 'LISTEN':
                open_ports.append(conn.laddr.port)
        suspicious = [p for p in psutil.process_iter(['name']) if 'malware' in p.info['name'].lower()]
        return {
            "open_ports": open_ports,
            "suspicious_processes": [p.info['name'] for p in suspicious],
            "recommendations": "Cerrar puertos no utilizados y actualizar software."
        }
        
    async def get_threats(self) -> Dict:
        # Placeholder
        return {"status": "no threats detected", "last_scan": "now"}