from PyQt6.QtWidgets import QMainWindow, QStackedWidget
from frontend.ui.hologram_widget import HologramWidget
from frontend.ui.dashboard import Dashboard
from frontend.ui.memory_panel import MemoryPanel
from frontend.ui.agents_panel import AgentsPanel
from frontend.ui.tasks_panel import TasksPanel
from frontend.ui.settings_panel import SettingsPanel

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("JARVIS-X")
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
        
    def show_hologram(self):
        self.stack.setCurrentWidget(self.hologram)