from typing import Dict, Set
from fastapi import WebSocket, WebSocketDisconnect
import json
from loguru import logger

class WebSocketManager:
    def __init__(self):
        self.active_connections: Dict[str, Set[WebSocket]] = {}
        
    async def connect(self, websocket: WebSocket):
        logger.info("WebSocket connection attempt...")
        try:
            # Aceptar la conexión sin verificar autenticación
            await websocket.accept()
            client_id = id(websocket)
            if "default" not in self.active_connections:
                self.active_connections["default"] = set()
            self.active_connections["default"].add(websocket)
            logger.info(f"WebSocket connected successfully: {client_id}")
            # Enviar mensaje de bienvenida
            await websocket.send_json({"type": "connected", "message": "Connected to JARVIS-X"})
        except Exception as e:
            logger.error(f"WebSocket accept error: {e}")
            raise
        
    def disconnect(self, websocket: WebSocket):
        for room in self.active_connections.values():
            if websocket in room:
                room.remove(websocket)
        logger.info(f"WebSocket disconnected")
        
    async def send_message(self, message: dict, room: str = "default"):
        if room in self.active_connections:
            for connection in self.active_connections[room]:
                try:
                    await connection.send_json(message)
                except Exception as e:
                    logger.error(f"Failed to send message: {e}")
                    
    async def handle_message(self, data: dict, websocket: WebSocket):
        logger.debug(f"Received message: {data}")
        msg_type = data.get("type")
        if msg_type == "ping":
            await websocket.send_json({"type": "pong"})
        elif msg_type == "voice_command":
            from backend.core.event_bus import event_bus
            await event_bus.emit("voice_command", data.get("data", {}))
        else:
            logger.warning(f"Unknown message type: {msg_type}")

websocket_manager = WebSocketManager()