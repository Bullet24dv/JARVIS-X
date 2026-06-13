import asyncio
import json
from PyQt6.QtWidgets import QMainWindow, QStackedWidget, QStatusBar
from PyQt6.QtCore import Qt, pyqtSignal, QObject, QTimer
from PyQt6.QtGui import QColor, QPalette
import qasync
import websockets

from .ui.hologram_widget import HologramWidget
from .ui.voice_visualizer import VoiceVisualizer
from .ui.dashboard import Dashboard
from .ui.memory_panel import MemoryPanel
from .ui.agents_panel import AgentsPanel
from .ui.tasks_panel import TasksPanel
from .ui.settings_panel import SettingsPanel


class WebSocketClient(QObject):
    message_received = pyqtSignal(dict)
    
    def __init__(self):
        super().__init__()
        self.websocket = None
        self.running = False
        
    async def connect(self):
        try:
            self.websocket = await websockets.connect("ws://127.0.0.1:8001")
            self.running = True
            asyncio.create_task(self._listen())
            return True
        except Exception as e:
            print(f"WebSocket connection failed: {e}")
            return False
        
    async def _listen(self):
        try:
            async for message in self.websocket:
                data = json.loads(message)
                self.message_received.emit(data)
        except Exception as e:
            print(f"WebSocket listen error: {e}")
        finally:
            self.running = False
            
    async def send(self, data):
        if self.websocket and self.running:
            try:
                await self.websocket.send(json.dumps(data))
            except Exception as e:
                print(f"WebSocket send error: {e}")
    
    async def close(self):
        self.running = False
        if self.websocket:
            await self.websocket.close()


class JarvisApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("JARVIS-X - Intelligent Assistant")
        self.setMinimumSize(1280, 720)
        self.setStyleSheet(self.load_stylesheet())
        
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(0, 0, 0, 200))
        self.setPalette(palette)
        
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)
        
        self.hologram = HologramWidget()
        self.dashboard = Dashboard()
        self.memory_panel = MemoryPanel()
        self.agents_panel = AgentsPanel()
        self.tasks_panel = TasksPanel()
        self.settings = SettingsPanel()
        
        self.stack.addWidget(self.hologram)
        self.stack.addWidget(self.dashboard)
        self.stack.addWidget(self.memory_panel)
        self.stack.addWidget(self.agents_panel)
        self.stack.addWidget(self.tasks_panel)
        self.stack.addWidget(self.settings)
        
        self.voice_viz = VoiceVisualizer(self)
        self.voice_viz.setGeometry(50, self.height()-150, self.width()-100, 100)
        
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage("Conectando a JARVIS-X...")
        
        self.ws_client = WebSocketClient()
        self.ws_client.message_received.connect(self.handle_ws_message)
        
        # Programar inicio asíncrono después de que el event loop esté activo
        QTimer.singleShot(100, self.start_async)
        
        self.show_hologram()
    
    def start_async(self):
        # Ahora sí podemos crear tareas asíncronas
        asyncio.create_task(self._init_websocket())
        
    async def _init_websocket(self):
        connected = await self.ws_client.connect()
        if connected:
            self.statusBar.showMessage("Conectado a JARVIS-X", 3000)
        else:
            self.statusBar.showMessage("Error de conexión - Backend no disponible", 5000)
        
    def load_stylesheet(self):
        try:
            with open("frontend/styles/main.qss", "r") as f:
                return f.read()
        except:
            return ""
            
    def show_hologram(self):
        self.stack.setCurrentWidget(self.hologram)
        
    def show_dashboard(self):
        self.stack.setCurrentWidget(self.dashboard)
        
    def handle_ws_message(self, data):
        if data.get("type") == "voice_response":
            self.voice_viz.show_response(data.get("text", ""))
        elif data.get("type") == "agent_status":
            self.agents_panel.update_status(data.get("agent", ""), data.get("status", ""))
            
    def resizeEvent(self, event):
        self.voice_viz.setGeometry(50, self.height()-150, self.width()-100, 100)
        super().resizeEvent(event)
    
    def closeEvent(self, event):
        # Cerrar WebSocket al salir (sin asyncio.create_task si no hay loop)
        # Podemos hacerlo síncrono o usar un timer
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                asyncio.create_task(self.ws_client.close())
        except:
            pass
        event.accept()