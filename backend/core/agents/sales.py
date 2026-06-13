from .base_agent import BaseAgent
from typing import Dict, Any

class SalesAgent(BaseAgent):
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        action = input_data.get("action")
        if action == "create_quote":
            return await self.create_quote(input_data["items"], input_data["customer"])
        elif action == "forecast":
            return await self.sales_forecast(input_data["historical_data"])
        return {"error": "Unknown action"}
        
    async def create_quote(self, items: list, customer: str) -> Dict:
        total = sum(item["price"] * item["quantity"] for item in items)
        prompt = f"Genera cotización formal para {customer} con items: {items}, total: {total}."
        quote = await self.think(prompt)
        return {"customer": customer, "total": total, "quote_text": quote}