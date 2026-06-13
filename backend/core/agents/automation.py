from .base_agent import BaseAgent
from typing import Dict, Any
import schedule
import asyncio

class AutomationAgent(BaseAgent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scheduled_tasks = {}
        
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        action = input_data.get("action")
        if action == "schedule":
            return await self.schedule_task(input_data["task"], input_data["cron"])
        elif action == "run_pipeline":
            return await self.run_automation(input_data["pipeline_name"])
        return {"error": "Unknown action"}
        
    async def schedule_task(self, task: str, cron: str) -> Dict:
        # Guardar en agenda
        self.scheduled_tasks[task] = cron
        prompt = f"Agendada tarea '{task}' con programación {cron}"
        return {"scheduled": True, "message": prompt}
        
    async def run_automation(self, pipeline_name: str) -> Dict:
        prompt = f"Ejecuta pipeline de automatización '{pipeline_name}' con las herramientas disponibles."
        result = await self.think(prompt)
        return {"pipeline": pipeline_name, "result": result}