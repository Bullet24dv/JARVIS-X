"""JARVIS-X Frontend Package"""
from .jarvis_app import JarvisApp
from .ui.hologram_widget import HologramWidget
from .ui.voice_visualizer import VoiceVisualizer
from .ui.dashboard import Dashboard
from .ui.memory_panel import MemoryPanel
from .ui.agents_panel import AgentsPanel
from .ui.tasks_panel import TasksPanel
from .ui.settings_panel import SettingsPanel

__all__ = [
    "JarvisApp",
    "HologramWidget",
    "VoiceVisualizer",
    "Dashboard",
    "MemoryPanel",
    "AgentsPanel",
    "TasksPanel",
    "SettingsPanel"
]