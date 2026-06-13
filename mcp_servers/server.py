import asyncio
import json
from aiohttp import web
from loguru import logger
from backend.core.mcp.mcp_server import MCPServer

routes = web.RouteTableDef()
mcp_server = MCPServer()

@routes.get("/tools")
async def list_tools(request):
    return web.json_response({"tools": list(mcp_server.connectors.keys())})

@routes.post("/call")
async def call_tool(request):
    data = await request.json()
    tool = data.get("tool")
    params = data.get("params", {})
    result = await mcp_server.execute_tool(tool, params)
    return web.json_response({"result": result})

async def start_mcp_server():
    await mcp_server.connect_all()
    app = web.Application()
    app.add_routes(routes)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 8080)
    await site.start()
    logger.info("MCP Server running on port 8080")
    await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(start_mcp_server())