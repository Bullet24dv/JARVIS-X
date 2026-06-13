"""MCP Connectors - Conectores para servicios externos"""
from .github import GitHubConnector
from .telegram import TelegramConnector
from .googledrive import GoogleDriveConnector
from .gmail import GmailConnector
from .calendar import CalendarConnector
from .notion import NotionConnector
from .slack import SlackConnector
from .discord import DiscordConnector
from .postgresql import PostgreSQLConnector
from .mysql import MySQLConnector
from .mongodb import MongoDBConnector
from .homeassistant import HomeAssistantConnector
from .local_fs import LocalFSConnector

__all__ = [
    "GitHubConnector",
    "TelegramConnector",
    "GoogleDriveConnector",
    "GmailConnector",
    "CalendarConnector",
    "NotionConnector",
    "SlackConnector",
    "DiscordConnector",
    "PostgreSQLConnector",
    "MySQLConnector",
    "MongoDBConnector",
    "HomeAssistantConnector",
    "LocalFSConnector"
]