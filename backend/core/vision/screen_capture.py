import pyautogui
import mss
import numpy as np
from PIL import Image
import asyncio
from loguru import logger

class ScreenCapture:
    def __init__(self):
        self.sct = mss.mss()
        
    async def capture_fullscreen(self) -> Image.Image:
        screenshot = pyautogui.screenshot()
        return screenshot
        
    async def capture_region(self, x: int, y: int, width: int, height: int) -> Image.Image:
        region = {"top": y, "left": x, "width": width, "height": height}
        img = self.sct.grab(region)
        return Image.frombytes("RGB", img.size, img.bgra, "raw", "BGRX")
        
    async def capture_window(self, window_title: str = None) -> Image.Image:
        if window_title:
            import pygetwindow as gw
            windows = gw.getWindowsWithTitle(window_title)
            if windows:
                win = windows[0]
                win.activate()
                await asyncio.sleep(0.2)
                return await self.capture_region(win.left, win.top, win.width, win.height)
        return await self.capture_fullscreen()
        
    async def capture_monitor(self, monitor_index: int = 1) -> Image.Image:
        monitors = self.sct.monitors
        if monitor_index < len(monitors):
            monitor = monitors[monitor_index]
            img = self.sct.grab(monitor)
            return Image.frombytes("RGB", img.size, img.bgra, "raw", "BGRX")
        return await self.capture_fullscreen()