from backend.core.mcp.connectors.telegram import TelegramConnector

class TelegramService:
    def __init__(self):
        self.connector = TelegramConnector()
        self.connected = False
        
    async def connect(self):
        if TelegramConnector.is_available():
            await self.connector.connect()
            self.connected = True
            
    async def send_message(self, chat_id: int, text: str):
        if self.connected:
            await self.connector.send_message(chat_id, text)
            
    def is_connected(self) -> bool:
        return self.connected