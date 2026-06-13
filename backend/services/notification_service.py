from backend.core.event_bus import event_bus
from loguru import logger

class NotificationService:
    def __init__(self):
        event_bus.on("notification", self._handle_notification)
        
    async def _handle_notification(self, data):
        logger.info(f"Notification: {data}")
        # Aquí se pueden enviar notificaciones a Telegram, Slack, etc.
        
    async def send(self, title: str, message: str, severity: str = "info"):
        await event_bus.emit("notification", {"title": title, "message": message, "severity": severity})