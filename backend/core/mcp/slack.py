import os
from slack_sdk.web.async_client import AsyncWebClient
from slack_sdk.socket_mode.aiohttp import SocketModeClient
from loguru import logger

class SlackConnector:
    def __init__(self):
        self.token = os.getenv("SLACK_BOT_TOKEN")
        self.app_token = os.getenv("SLACK_APP_TOKEN")
        self.client = None
        self.socket_client = None
        
    @classmethod
    def is_available(cls):
        return bool(os.getenv("SLACK_BOT_TOKEN") and os.getenv("SLACK_APP_TOKEN"))
        
    async def connect(self):
        self.client = AsyncWebClient(token=self.token)
        self.socket_client = SocketModeClient(
            app_token=self.app_token,
            web_client=self.client
        )
        await self.socket_client.connect()
        logger.info("Slack connector initialized")
        
    async def send_message(self, channel: str, text: str) -> dict:
        return await self.client.chat_postMessage(channel=channel, text=text)
        
    async def disconnect(self):
        await self.socket_client.close()