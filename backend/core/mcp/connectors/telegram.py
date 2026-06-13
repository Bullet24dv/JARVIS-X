import os
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram import Update
import asyncio
from loguru import logger

class TelegramConnector:
    def __init__(self):
        self.token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.application = None
        self.message_queue = asyncio.Queue()
        
    @classmethod
    def is_available(cls):
        return bool(os.getenv("TELEGRAM_BOT_TOKEN"))
        
    async def connect(self):
        self.application = Application.builder().token(self.token).build()
        
        async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
            await update.message.reply_text("🤖 JARVIS-X conectado. Envíame comandos.")
            
        async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
            await update.message.reply_text("✅ Sistema operativo. Todos los servicios activos.")
            
        async def screenshot(update: Update, context: ContextTypes.DEFAULT_TYPE):
            import pyautogui
            screenshot = pyautogui.screenshot()
            screenshot.save("temp_screenshot.png")
            with open("temp_screenshot.png", "rb") as f:
                await update.message.reply_photo(f)
                
        async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
            from backend.core.event_bus import event_bus
            await event_bus.emit("telegram_message", {"text": update.message.text, "chat_id": update.effective_chat.id})
            await update.message.reply_text("🔄 Procesando...")
            
        self.application.add_handler(CommandHandler("start", start))
        self.application.add_handler(CommandHandler("status", status))
        self.application.add_handler(CommandHandler("screenshot", screenshot))
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        
        asyncio.create_task(self.application.run_polling())
        logger.info("Telegram bot started")
        
    async def send_message(self, chat_id: int, text: str):
        await self.application.bot.send_message(chat_id=chat_id, text=text)
        
    async def disconnect(self):
        if self.application:
            await self.application.shutdown()