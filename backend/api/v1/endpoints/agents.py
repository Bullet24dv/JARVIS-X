from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.services.agent_service import AgentService

router = APIRouter()
agent_service = AgentService()

class AgentTask(BaseModel):
    agent_name: str
    action: str
    params: dict = {}

@router.post("/{agent_name}/task")
async def run_agent_task(agent_name: str, task: AgentTask):
    result = await agent_service.run_agent(agent_name, task.action, task.params)
    return result

@router.get("/list")
async def list_agents():
    agents = await agent_service.list_agents()
    return {"agents": agents}

@router.post("/orchestrate")
async def orchestrate(task_description: str):
    result = await agent_service.orchestrate(task_description)
    return result