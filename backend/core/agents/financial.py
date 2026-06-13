from .base_agent import BaseAgent
from typing import Dict, Any

class FinancialAgent(BaseAgent):
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        action = input_data.get("action")
        if action == "calculate_budget":
            return await self.budget_calculation(input_data["income"], input_data["expenses"])
        elif action == "investment_suggestion":
            return await self.suggest_investment(input_data["amount"], input_data["risk_profile"])
        return {"error": "Unknown action"}
        
    async def budget_calculation(self, income: float, expenses: Dict[str, float]) -> Dict:
        total_expenses = sum(expenses.values())
        remaining = income - total_expenses
        prompt = f"Ingreso: {income}, gastos: {expenses}, restante: {remaining}. Sugiere ajustes financieros."
        advice = await self.think(prompt)
        return {"remaining": remaining, "advice": advice}
        
    async def suggest_investment(self, amount: float, risk_profile: str) -> Dict:
        prompt = f"Con {amount} CLP y perfil {risk_profile}, recomienda 3 opciones de inversión en Chile."
        suggestions = await self.think(prompt)
        return {"amount": amount, "risk": risk_profile, "suggestions": suggestions}