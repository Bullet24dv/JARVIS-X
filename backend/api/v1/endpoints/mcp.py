from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.services.mcp_service import MCPService

router = APIRouter()
mcp_service = MCPService()

class MCPToolRequest(BaseModel):
    tool: str
    params: dict = {}

@router.post("/execute")
async def execute_tool(request: MCPToolRequest):
    result = await mcp_service.execute_tool(request.tool, request.params)
    return result

@router.get("/connectors")
async def list_connectors():
    connectors = await mcp_service.list_connectors()
    return {"connectors": connectors}