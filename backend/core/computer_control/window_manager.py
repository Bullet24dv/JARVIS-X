import pygetwindow as gw
from typing import List, Dict, Optional

class WindowManager:
    @staticmethod
    def list_windows() -> List[Dict]:
        windows = []
        for win in gw.getAllWindows():
            if win.title:
                windows.append({
                    "title": win.title,
                    "left": win.left,
                    "top": win.top,
                    "width": win.width,
                    "height": win.height,
                    "is_active": win.isActive
                })
        return windows
        
    @staticmethod
    def get_window_by_title(title: str) -> Optional[gw.Window]:
        windows = gw.getWindowsWithTitle(title)
        return windows[0] if windows else None
        
    @staticmethod
    def activate_window(title: str):
        win = WindowManager.get_window_by_title(title)
        if win:
            win.activate()
            
    @staticmethod
    def resize_window(title: str, width: int, height: int):
        win = WindowManager.get_window_by_title(title)
        if win:
            win.resize(width, height)