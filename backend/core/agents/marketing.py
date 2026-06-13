from .base_agent import BaseAgent
from typing import Dict, Any

class MarketingAgent(BaseAgent):
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        action = input_data.get("action")
        if action == "create_campaign":
            return await self.create_campaign(input_data["product"], input_data["budget"])
        elif action == "social_media_post":
            return await self.generate_post(input_data["topic"])
        return {"error": "Unknown action"}
        
    async def create_campaign(self, product: str, budget: float) -> Dict:
        prompt = f"Crea una estrategia de campaña para {product} con presupuesto ${budget}. Define canales, público objetivo y KPI."
        strategy = await self.think(prompt)
        return {"product": product, "budget": budget, "strategy": strategy}
        
    async def generate_post(self, topic: str) -> str:
        prompt = f"Escribe un post para redes sociales (Instagram/LinkedIn) sobre {topic}, tono profesional y atractivo."
        return await self.think(prompt)