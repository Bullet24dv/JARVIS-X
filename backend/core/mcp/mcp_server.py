import asyncio
import json
from typing import Dict, Any, Optional
from loguru import logger
from .connectors.github import GitHubConnector
from .connectors.telegram import TelegramConnector
from .connectors.googledrive import GoogleDriveConnector
from .connectors.gmail import GmailConnector
from .connectors.calendar import CalendarConnector
from .connectors.notion import NotionConnector
from .connectors.slack import SlackConnector
from .connectors.discord import DiscordConnector
from .connectors.postgresql import PostgreSQLConnector
from .connectors.mysql import MySQLConnector
from .connectors.mongodb import MongoDBConnector
from .connectors.homeassistant import HomeAssistantConnector
from .connectors.local_fs import LocalFSConnector

class MCPServer:
    """Model Context Protocol Server - Conecta con servicios externos."""
    
    def __init__(self):
        self.connectors = {}
        
    async def connect_all(self):
        """Inicializa todos los conectores configurados."""
        # Conectores con autenticación opcional
        if GitHubConnector.is_available():
            self.connectors["github"] = GitHubConnector()
            await self.connectors["github"].connect()
        if TelegramConnector.is_available():
            self.connectors["telegram"] = TelegramConnector()
            await self.connectors["telegram"].connect()
        if GoogleDriveConnector.is_available():
            self.connectors["googledrive"] = GoogleDriveConnector()
            await self.connectors["googledrive"].connect()
        if GmailConnector.is_available():
            self.connectors["gmail"] = GmailConnector()
            await self.connectors["gmail"].connect()
        if CalendarConnector.is_available():
            self.connectors["calendar"] = CalendarConnector()
            await self.connectors["calendar"].connect()
        if NotionConnector.is_available():
            self.connectors["notion"] = NotionConnector()
            await self.connectors["notion"].connect()
        if SlackConnector.is_available():
            self.connectors["slack"] = SlackConnector()
            await self.connectors["slack"].connect()
        if DiscordConnector.is_available():
            self.connectors["discord"] = DiscordConnector()
            await self.connectors["discord"].connect()
        if PostgreSQLConnector.is_available():
            self.connectors["postgres"] = PostgreSQLConnector()
            await self.connectors["postgres"].connect()
        if MySQLConnector.is_available():
            self.connectors["mysql"] = MySQLConnector()
            await self.connectors["mysql"].connect()
        if MongoDBConnector.is_available():
            self.connectors["mongodb"] = MongoDBConnector()
            await self.connectors["mongodb"].connect()
        if HomeAssistantConnector.is_available():
            self.connectors["homeassistant"] = HomeAssistantConnector()
            await self.connectors["homeassistant"].connect()
        # Siempre disponible
        self.connectors["localfs"] = LocalFSConnector()
        await self.connectors["localfs"].connect()
        
        logger.info(f"MCP Server initialized with {len(self.connectors)} connectors")
        
    async def disconnect_all(self):
        for connector in self.connectors.values():
            await connector.disconnect()
            
    async def execute_tool(self, tool_name: str, params: Dict) -> Any:
        """Ejecuta una herramienta MCP."""
        # Formato: "connector.action"
        if "." not in tool_name:
            raise ValueError(f"Invalid tool name: {tool_name}")
        conn_name, action = tool_name.split(".", 1)
        connector = self.connectors.get(conn_name)
        if not connector:
            raise Exception(f"Connector {conn_name} not found")
        method = getattr(connector, action, None)
        if not method:
            raise Exception(f"Action {action} not found in {conn_name}")
        return await method(**params)