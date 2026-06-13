import os
import discord
from discord.ext import commands
from typing import Dict, Any, Optional
from loguru import logger

class DiscordConnector:
    def __init__(self):
        self.token = os.getenv("DISCORD_BOT_TOKEN")
        self.bot: Optional[commands.Bot] = None
        self.is_connected = False
        
    @classmethod
    def is_available(cls) -> bool:
        return bool(os.getenv("DISCORD_BOT_TOKEN"))
    
    async def connect(self) -> bool:
        if not self.is_available():
            logger.warning("Discord token not configured")
            return False
        
        try:
            intents = discord.Intents.default()
            intents.message_content = True
            intents.members = True
            
            self.bot = commands.Bot(command_prefix="!", intents=intents)
            
            @self.bot.event
            async def on_ready():
                self.is_connected = True
                logger.info(f"Discord bot logged as {self.bot.user}")
            
            await self.bot.start(self.token)
            return True
        except Exception as e:
            logger.error(f"Failed to connect Discord: {e}")
            return False
    
    async def send_message(self, channel_id: int, text: str) -> Dict[str, Any]:
        if not self.is_connected:
            await self.connect()
        
        try:
            channel = self.bot.get_channel(channel_id)
            if not channel:
                return {"success": False, "error": "Channel not found"}
            
            await channel.send(text)
            return {"success": True, "channel_id": channel_id}
        except Exception as e:
            logger.error(f"Failed to send Discord message: {e}")
            return {"success": False, "error": str(e)}
    
    async def send_embed(self, channel_id: int, title: str, description: str, color: int = 0x00ffff) -> Dict[str, Any]:
        if not self.is_connected:
            await self.connect()
        
        try:
            channel = self.bot.get_channel(channel_id)
            if not channel:
                return {"success": False, "error": "Channel not found"}
            
            embed = discord.Embed(title=title, description=description, color=color)
            await channel.send(embed=embed)
            return {"success": True, "channel_id": channel_id}
        except Exception as e:
            logger.error(f"Failed to send Discord embed: {e}")
            return {"success": False, "error": str(e)}
    
    async def disconnect(self) -> None:
        if self.bot:
            await self.bot.close()
        self.is_connected = False
        logger.info("Discord connector disconnected")