from backend.core.llm_router import LLMRouter
from loguru import logger

class ProgrammerMode:
    def __init__(self, llm_router: LLMRouter):
        self.llm = llm_router
        
    async def generate_api(self, specification: str) -> str:
        prompt = f"""Genera una API REST completa usando FastAPI según esta especificación:
        {specification}
        Incluye:
        - Modelos Pydantic
        - Endpoints CRUD
        - Autenticación básica
        - Documentación Swagger
        Devuelve solo el código Python."""
        response = await self.llm.chat_completion([{"role": "user", "content": prompt}])
        return response["content"]
        
    async def generate_documentation(self, code: str) -> str:
        prompt = f"""Genera documentación profesional en español para el siguiente código:
        {code}
        Incluye: descripción, instalación, uso, ejemplos."""
        response = await self.llm.chat_completion([{"role": "user", "content": prompt}])
        return response["content"]
        
    async def review_code(self, code: str) -> dict:
        prompt = f"""Revisa el siguiente código y encuentra:
        1. Errores potenciales
        2. Vulnerabilidades de seguridad
        3. Mejoras de rendimiento
        4. Violaciones de estilo PEP 8
        Código:
        {code}"""
        response = await self.llm.chat_completion([{"role": "user", "content": prompt}])
        return {"review": response["content"]}