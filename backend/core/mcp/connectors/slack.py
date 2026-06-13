import os
import json
from typing import Dict, Any, Optional
from loguru import logger
from slack_sdk.web.async_client import AsyncWebClient
from slack_sdk.socket_mode.aiohttp import SocketModeClient
from slack_sdk.socket_mode.request import SocketModeRequest

class SlackConnector:
    def __init__(self):
        self.bot_token = os.getenv("SLACK_BOT_TOKEN")
        self.app_token = os.getenv("SLACK_APP_TOKEN")
        self.client: Optional[AsyncWebClient] = None
        self.socket_client: Optional[SocketModeClient] = None
        self.is_connected = False
        
    @classmethod
    def is_available(cls) -> bool:
        return bool(os.getenv("SLACK_BOT_TOKEN") and os.getenv("SLACK_APP_TOKEN"))
    
    async def connect(self) -> bool:
        if not self.is_available():
            logger.warning("Slack credentials not configured")
            return False
        
        try:
            self.client = AsyncWebClient(token=self.bot_token)
            self.socket_client = SocketModeClient(
                app_token=self.app_token,
                web_client=self.client
            )
            await self.socket_client.connect()
            self.is_connected = True
            logger.info("Slack connector connected successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to connect Slack: {e}")
            return False
    
    async def send_message(self, channel: str, text: str, thread_ts: Optional[str] = None) -> Dict[str, Any]:
        if not self.is_connected:
            await self.connect()
        
        try:
            response = await self.client.chat_postMessage(
                channel=channel,
                text=text,
                thread_ts=thread_ts
            )
            return {"success": True, "ts": response["ts"], "channel": response["channel"]}
        except Exception as e:
            logger.error(f"Failed to send Slack message: {e}")
            return {"success": False, "error": str(e)}
    
    async def send_file(self, channel: str, file_path: str, comment: str = "") -> Dict[str, Any]:
        if not self.is_connected:
            await self.connect()
        
        try:
            response = await self.client.files_upload_v2(
                channel=channel,
                file=file_path,
                initial_comment=comment
            )
            return {"success": True, "file_id": response.get("file", {}).get("id")}
        except Exception as e:
            logger.error(f"Failed to send Slack file: {e}")
            return {"success": False, "error": str(e)}
    
    async def get_channels(self) -> list:
        if not self.is_connected:
            await self.connect()
        
        try:
            response = await self.client.conversations_list(types="public_channel,private_channel")
            return response.get("channels", [])
        except Exception as e:
            logger.error(f"Failed to get Slack channels: {e}")
            return []
    
    async def disconnect(self) -> None:
        if self.socket_client:
            await self.socket_client.close()
        self.is_connected = False
        logger.info("Slack connector disconnected")