import subprocess
import ast
import black
import autopep8
from pathlib import Path
from typing import Dict, Any
from loguru import logger
from .base_agent import BaseAgent

class ProgrammerAgent(BaseAgent):
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        action = input_data.get("action")
        if action == "create_app":
            return await self.create_application(input_data["specification"])
        elif action == "fix_code":
            return await self.fix_code(input_data["file_path"], input_data["error"])
        elif action == "analyze_repo":
            return await self.analyze_repository(input_data["repo_path"])
        else:
            return {"error": "Unknown action"}
            
    async def create_application(self, spec: str) -> Dict:
        prompt = f"""Genera una aplicación completa en Python según esta especificación: {spec}
        Incluye:
        - Estructura de archivos
        - Código fuente completo
        - requirements.txt
        - README
        Responde con el código formateado."""
        response = await self.think(prompt)
        # Extraer y guardar archivos
        return {"message": "Aplicación generada", "code": response}
        
    async def fix_code(self, file_path: str, error: str) -> Dict:
        with open(file_path, "r") as f:
            code = f.read()
        prompt = f"El siguiente código tiene el error: {error}. Corrígelo y devuelve el código completo.\n\n{code}"
        fixed_code = await self.think(prompt)
        # Aplicar formateo automático
        fixed_code = autopep8.fix_code(fixed_code)
        # Guardar backup
        backup_path = Path(file_path).with_suffix(".bak")
        Path(file_path).rename(backup_path)
        with open(file_path, "w") as f:
            f.write(fixed_code)
        return {"fixed": True, "backup": str(backup_path)}
        
    async def analyze_repository(self, repo_path: str) -> Dict:
        # Escanear estructura, detectar errores comunes
        analysis = {
            "files": [],
            "issues": [],
            "suggestions": []
        }
        path = Path(repo_path)
        for py_file in path.rglob("*.py"):
            analysis["files"].append(str(py_file))
            try:
                with open(py_file, "r") as f:
                    ast.parse(f.read())
            except SyntaxError as e:
                analysis["issues"].append(f"{py_file}: {e}")
        return analysis