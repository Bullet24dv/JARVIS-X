from .base_agent import BaseAgent
from typing import Dict, Any
import pandas as pd
import json

class AnalystAgent(BaseAgent):
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        action = input_data.get("action")
        if action == "analyze_data":
            return await self.analyze_data(input_data["data"], input_data.get("question"))
        elif action == "generate_report":
            return await self.generate_report(input_data["data"])
        return {"error": "Unknown action"}
        
    async def analyze_data(self, data: Any, question: str = None) -> Dict:
        # Si es CSV o JSON, cargar
        if isinstance(data, str):
            if data.endswith('.csv'):
                df = pd.read_csv(data)
            elif data.endswith('.json'):
                with open(data) as f:
                    df = pd.json_normalize(json.load(f))
            else:
                df = None
        else:
            df = pd.DataFrame(data) if isinstance(data, dict) else None
            
        if df is None:
            return {"error": "Unsupported data format"}
            
        prompt = f"Analiza estos datos y responde: {question if question else 'Haz un resumen ejecutivo'}\n\n{df.head(10).to_string()}"
        analysis = await self.think(prompt)
        return {
            "shape": df.shape,
            "columns": list(df.columns),
            "analysis": analysis,
            "head": df.head(5).to_dict()
        }