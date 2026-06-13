# ============================================================
# JARVIS-X | backend/core/agents/orchestrator.py
# Orquestador del sistema multiagente
# ============================================================

import asyncio
import logging
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Callable, Dict, List, Optional

from backend.config import settings
from backend.core.llm_router import LLMRouter, LLMMessage
from backend.core.memory.manager import MemoryManager

logger = logging.getLogger("jarvis.orchestrator")


class AgentType(str, Enum):
    PROGRAMADOR = "programador"
    INVESTIGADOR = "investigador"
    ANALISTA = "analista"
    FINANCIERO = "financiero"
    MARKETING = "marketing"
    VENTAS = "ventas"
    AUTOMATIZACION = "automatizacion"
    SEGURIDAD = "seguridad"
    DOMOTICA = "domotica"
    STARCARS = "starcars"
    ORQUESTADOR = "orquestador"


class TaskStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    DELEGATED = "delegated"


@dataclass
class AgentTask:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    description: str = ""
    assigned_agent: Optional[str] = None
    status: TaskStatus = TaskStatus.PENDING
    result: Optional[str] = None
    error: Optional[str] = None
    subtasks: List["AgentTask"] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    completed_at: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "description": self.description,
            "assigned_agent": self.assigned_agent,
            "status": self.status,
            "result": self.result,
            "error": self.error,
            "subtasks": [s.to_dict() for s in self.subtasks],
            "created_at": self.created_at,
            "completed_at": self.completed_at,
        }


class BaseAgent:
    """Agente base con memoria propia y capacidad de delegación."""

    SYSTEM_PROMPTS: Dict[str, str] = {
        AgentType.PROGRAMADOR: (
            "Eres el agente programador de JARVIS. Especialista en Python, JavaScript, "
            "arquitectura de software, debugging y generación de código. Escribes código "
            "limpio, documentado y funcional. Hablas en español latino."
        ),
        AgentType.INVESTIGADOR: (
            "Eres el agente investigador de JARVIS. Especialista en búsqueda de información, "
            "análisis de fuentes, síntesis de datos y generación de reportes completos. "
            "Hablas en español latino."
        ),
        AgentType.ANALISTA: (
            "Eres el agente analista de JARVIS. Especialista en análisis de datos, "
            "estadísticas, visualizaciones e insights de negocio. Hablas en español latino."
        ),
        AgentType.FINANCIERO: (
            "Eres el agente financiero de JARVIS. Especialista en finanzas, inversiones, "
            "presupuestos, cálculos financieros y análisis de mercados. Hablas en español latino."
        ),
        AgentType.MARKETING: (
            "Eres el agente de marketing de JARVIS. Especialista en estrategias de marketing, "
            "contenido, redes sociales, SEO y campañas publicitarias. Hablas en español latino."
        ),
        AgentType.VENTAS: (
            "Eres el agente de ventas de JARVIS. Especialista en estrategias de ventas, "
            "argumentación, CRM, seguimiento de prospectos y cierre de negocios. Hablas en español latino."
        ),
        AgentType.AUTOMATIZACION: (
            "Eres el agente de automatización de JARVIS. Especialista en scripts, "
            "automatización web con Playwright/Selenium, flujos de trabajo y procesos repetitivos. "
            "Hablas en español latino."
        ),
        AgentType.SEGURIDAD: (
            "Eres el agente de seguridad de JARVIS. Especialista en ciberseguridad, "
            "auditorías, detección de vulnerabilidades y mejores prácticas de seguridad. "
            "Hablas en español latino."
        ),
        AgentType.DOMOTICA: (
            "Eres el agente de domótica de JARVIS. Especialista en automatización del hogar, "
            "Home Assistant, dispositivos inteligentes y protocolos IoT. Hablas en español latino."
        ),
        AgentType.STARCARS: (
            "Eres el agente StarCars de JARVIS. Especialista en el sector automotriz: "
            "publicación de vehículos, descripciones comerciales, financiamiento, cotizaciones "
            "y marketing automotriz. Hablas en español latino."
        ),
    }

    def __init__(
        self,
        agent_type: AgentType,
        llm_router: LLMRouter,
        memory: MemoryManager,
        delegate_fn: Optional[Callable] = None,
    ):
        self.type = agent_type
        self.name = agent_type.value
        self._llm = llm_router
        self._memory = memory
        self._delegate = delegate_fn
        self._system_prompt = self.SYSTEM_PROMPTS.get(agent_type, "Eres JARVIS, asistente IA.")
        self._task_history: List[AgentTask] = []

    async def execute(self, task: AgentTask, context: str = "") -> str:
        """Ejecuta una tarea y retorna el resultado."""
        task.status = TaskStatus.RUNNING
        task.assigned_agent = self.name
        logger.info(f"[{self.name.upper()}] Ejecutando: {task.description[:100]}")

        try:
            # Recuperar contexto de memoria del agente
            agent_memory = await self._memory.search_memory(
                query=task.description,
                top_k=3,
                memory_type=f"agent_{self.name}",
            )

            # Construir prompt
            memory_ctx = ""
            if agent_memory:
                memory_ctx = "\n".join(f"- {m['content'][:200]}" for m in agent_memory)
                memory_ctx = f"\n\n[MEMORIA DEL AGENTE]\n{memory_ctx}"

            user_prompt = f"{task.description}"
            if context:
                user_prompt += f"\n\n[CONTEXTO ADICIONAL]\n{context}"
            if memory_ctx:
                user_prompt += memory_ctx

            messages = [LLMMessage(role="user", content=user_prompt)]

            response = await self._llm.chat(
                messages=messages,
                system_override=self._system_prompt,
                temperature=0.5,
                max_tokens=2048,
            )

            result = response.content
            task.status = TaskStatus.COMPLETED
            task.result = result
            task.completed_at = datetime.now(timezone.utc).isoformat()

            # Guardar resultado en memoria del agente
            await self._memory.save_to_long_term(
                content=f"TAREA: {task.description}\nRESULTADO: {result[:500]}",
                memory_type=f"agent_{self.name}",
                metadata={"task_id": task.id, "agent": self.name},
            )

            self._task_history.append(task)
            return result

        except Exception as e:
            task.status = TaskStatus.FAILED
            task.error = str(e)
            logger.error(f"[{self.name.upper()}] Error en tarea: {e}")
            raise

    def get_stats(self) -> Dict:
        completed = sum(1 for t in self._task_history if t.status == TaskStatus.COMPLETED)
        failed = sum(1 for t in self._task_history if t.status == TaskStatus.FAILED)
        return {
            "name": self.name,
            "total_tasks": len(self._task_history),
            "completed": completed,
            "failed": failed,
        }


class AgentOrchestrator:
    """
    Orquestador del sistema multiagente.
    - Clasifica intenciones y delega al agente apropiado
    - Ejecuta tareas en paralelo cuando es posible
    - Coordina colaboración entre agentes
    - Mantiene historial de tareas
    """

    # Keywords para routing de intenciones
    INTENT_ROUTING: Dict[str, List[str]] = {
        AgentType.PROGRAMADOR: [
            "código", "programa", "script", "función", "clase", "bug", "error",
            "python", "javascript", "api", "base de datos", "sql", "algoritmo",
            "implementa", "desarrolla", "crea el código",
        ],
        AgentType.INVESTIGADOR: [
            "investiga", "busca información", "encuentra", "qué es", "cómo funciona",
            "explica", "informe", "reporte", "analiza", "investiga sobre",
        ],
        AgentType.ANALISTA: [
            "analiza", "datos", "estadísticas", "gráfico", "tendencia",
            "métricas", "kpi", "dashboard", "excel", "csv",
        ],
        AgentType.FINANCIERO: [
            "finanzas", "inversión", "presupuesto", "dinero", "costo", "precio",
            "cotización", "cuota", "pago", "rentabilidad", "roi",
        ],
        AgentType.MARKETING: [
            "marketing", "publicidad", "redes sociales", "contenido", "campaña",
            "seo", "instagram", "facebook", "tiktok", "post", "estrategia de marca",
        ],
        AgentType.VENTAS: [
            "ventas", "cliente", "propuesta", "oferta", "vender", "prospecto",
            "seguimiento", "crm", "negociación", "cierre",
        ],
        AgentType.AUTOMATIZACION: [
            "automatiza", "selenium", "playwright", "web scraping", "formulario",
            "descarga", "publica automáticamente", "bot", "flujo de trabajo",
        ],
        AgentType.SEGURIDAD: [
            "seguridad", "vulnerabilidad", "contraseña", "cifra", "hack",
            "firewall", "auditoría", "acceso", "permiso", "certificado",
        ],
        AgentType.DOMOTICA: [
            "home assistant", "domótica", "smart home", "luz", "temperatura",
            "sensor", "dispositivo inteligente", "alexa", "zigbee", "mqtt",
        ],
        AgentType.STARCARS: [
            "vehículo", "auto", "carro", "starcars", "automotora", "publicar vehículo",
            "financiamiento auto", "marca", "modelo", "kilometraje",
        ],
    }

    def __init__(self, llm_router: LLMRouter, memory: MemoryManager):
        self._llm = llm_router
        self._memory = memory
        self._agents: Dict[str, BaseAgent] = {}
        self._active_tasks: Dict[str, AgentTask] = {}
        self._semaphore = asyncio.Semaphore(settings.AGENT_PARALLEL_LIMIT)

    async def initialize(self):
        """Inicializa todos los agentes especializados."""
        for agent_type in AgentType:
            if agent_type == AgentType.ORQUESTADOR:
                continue
            self._agents[agent_type.value] = BaseAgent(
                agent_type=agent_type,
                llm_router=self._llm,
                memory=self._memory,
                delegate_fn=self.delegate_task,
            )
        logger.info(f"Agentes iniciados: {list(self._agents.keys())}")

    def _classify_intent(self, query: str) -> Optional[str]:
        """Clasifica la intención y retorna el tipo de agente más adecuado."""
        query_lower = query.lower()
        scores: Dict[str, int] = {}

        for agent_type, keywords in self.INTENT_ROUTING.items():
            score = sum(1 for kw in keywords if kw in query_lower)
            if score > 0:
                scores[agent_type] = score

        if not scores:
            return None

        return max(scores, key=lambda k: scores[k])

    async def process(
        self,
        query: str,
        context: str = "",
        force_agent: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Procesa una consulta:
        1. Clasifica la intención
        2. Delega al agente apropiado (o JARVIS directo si es conversación general)
        3. Retorna el resultado
        """
        task = AgentTask(description=query)
        self._active_tasks[task.id] = task

        # Determinar agente
        agent_type = force_agent or self._classify_intent(query)

        if agent_type and agent_type in self._agents:
            agent = self._agents[agent_type]
            async with self._semaphore:
                result = await agent.execute(task, context=context)
            source = agent_type
        else:
            # Respuesta directa de JARVIS (conversación general)
            result = await self._jarvis_direct_response(query, context)
            task.status = TaskStatus.COMPLETED
            task.result = result
            source = "jarvis"

        self._active_tasks.pop(task.id, None)

        return {
            "task_id": task.id,
            "agent": source,
            "result": result,
            "status": task.status,
        }

    async def _jarvis_direct_response(self, query: str, context: str = "") -> str:
        """Respuesta directa de JARVIS para conversaciones generales."""
        enriched = await self._memory.get_enriched_context(query)

        system = settings.JARVIS_PERSONA
        if enriched:
            system += f"\n\n[CONTEXTO DE MEMORIA]\n{enriched}"
        if context:
            system += f"\n\n[CONTEXTO ACTUAL]\n{context}"

        messages = self._memory.get_short_term_as_messages(last_n=10)
        messages.append({"role": "user", "content": query})

        llm_messages = [LLMMessage(role=m["role"], content=m["content"]) for m in messages]

        response = await self._llm.chat(
            messages=llm_messages,
            system_override=system,
            temperature=0.8,
        )

        # Guardar en memoria corto plazo
        self._memory.add_turn("user", query)
        self._memory.add_turn("assistant", response.content)

        # Guardar en memoria larga si parece importante
        if len(query) > 50:
            await self._memory.save_to_long_term(
                content=f"Usuario: {query}\nJARVIS: {response.content[:300]}",
                memory_type="conversation",
            )

        return response.content

    async def delegate_task(self, description: str, to_agent: str, context: str = "") -> str:
        """Delega una subtarea a otro agente."""
        if to_agent not in self._agents:
            return f"Agente '{to_agent}' no disponible."
        task = AgentTask(description=description)
        async with self._semaphore:
            return await self._agents[to_agent].execute(task, context=context)

    async def run_parallel_tasks(self, tasks: List[Dict[str, str]]) -> List[Dict]:
        """Ejecuta múltiples tareas en paralelo."""
        async def run_one(t: Dict) -> Dict:
            result = await self.process(t["query"], force_agent=t.get("agent"))
            return result

        results = await asyncio.gather(*[run_one(t) for t in tasks], return_exceptions=True)
        return [
            r if isinstance(r, dict) else {"error": str(r)}
            for r in results
        ]

    def get_status(self) -> Dict[str, Any]:
        return {
            "agents": {name: agent.get_stats() for name, agent in self._agents.items()},
            "active_tasks": len(self._active_tasks),
        }

    async def shutdown(self):
        logger.info("Orquestador apagado.")