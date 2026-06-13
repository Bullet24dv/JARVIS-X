from typing import Dict, Any, Optional
from loguru import logger
from .base_agent import BaseAgent
from .programmer import ProgrammerAgent
from .researcher import ResearcherAgent
from .analyst import AnalystAgent
from .financial import FinancialAgent
from .marketing import MarketingAgent
from .sales import SalesAgent
from .automation import AutomationAgent
from .security import SecurityAgent
from .smart_home import SmartHomeAgent
from .starcars import StarCarsAgent
from backend.core.llm_router import LLMRouter
from backend.core.memory.vector_store import VectorMemory

class AgentOrchestrator:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
        
    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.agents = {}
            self.llm_router = None
            self.memory = None
            self.initialized = False
            
    async def initialize(self, llm_router: LLMRouter, memory: VectorMemory):
        if self.initialized:
            return
        self.llm_router = llm_router
        self.memory = memory
        
        # Inicializar agentes
        self.agents["programmer"] = ProgrammerAgent("Programador", "Desarrollar software y corregir errores", llm_router, memory)
        self.agents["researcher"] = ResearcherAgent("Investigador", "Buscar información y analizar datos", llm_router, memory)
        self.agents["analyst"] = AnalystAgent("Analista", "Analizar datos y generar reportes", llm_router, memory)
        self.agents["financial"] = FinancialAgent("Financiero", "Gestionar finanzas y presupuestos", llm_router, memory)
        self.agents["marketing"] = MarketingAgent("Marketing", "Crear estrategias de marketing", llm_router, memory)
        self.agents["sales"] = SalesAgent("Ventas", "Gestionar ventas y clientes", llm_router, memory)
        self.agents["automation"] = AutomationAgent("Automatización", "Automatizar tareas repetitivas", llm_router, memory)
        self.agents["security"] = SecurityAgent("Seguridad", "Monitorear seguridad del sistema", llm_router, memory)
        self.agents["smart_home"] = SmartHomeAgent("Domótica", "Controlar dispositivos del hogar", llm_router, memory)
        self.agents["starcars"] = StarCarsAgent("StarCars", "Gestionar publicaciones automotrices", llm_router, memory)
        
        self.initialized = True
        logger.info(f"Agent orchestrator initialized with {len(self.agents)} agents")
        
    async def delegate(self, agent_name: str, task: Dict[str, Any]) -> Dict[str, Any]:
        agent = self.agents.get(agent_name)
        if not agent:
            return {"error": f"Agent {agent_name} not found"}
        logger.info(f"Delegating task to {agent_name}: {task.get('action')}")
        return await agent.process(task)
        
    async def route_task(self, task_description: str) -> Dict[str, Any]:
        """Usa LLM para determinar qué agente debe manejar la tarea."""
        prompt = f"Determina qué agente debe ejecutar esta tarea. Agentes disponibles: {', '.join(self.agents.keys())}. Tarea: {task_description}. Responde solo con el nombre del agente."
        response = await self.llm_router.chat_completion([{"role": "user", "content": prompt}])
        agent_name = response["content"].strip().lower()
        return {"agent": agent_name if agent_name in self.agents else "analyst", "task": task_description}