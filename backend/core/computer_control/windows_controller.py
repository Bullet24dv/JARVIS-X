import subprocess
import psutil
import pyautogui
import asyncio
from typing import List, Dict
import os
from loguru import logger

class WindowsController:
    def __init__(self):
        pass
        
    async def open_app(self, app_name: str) -> bool:
        try:
            # Manejar casos especiales
            app_map = {
                "chrome": "chrome",
                "navegador": "chrome",
                "firefox": "firefox",
                "explorador": "explorer",
                "bloc de notas": "notepad",
                "calculadora": "calc",
                "cmd": "cmd",
                "terminal": "cmd"
            }
            cmd = app_map.get(app_name.lower(), app_name)
            subprocess.Popen(cmd, shell=True)
            logger.info(f"Opened {app_name}")
            return True
        except Exception as e:
            logger.error(f"Failed to open {app_name}: {e}")
            return False
            
    async def close_app(self, app_name: str) -> bool:
        for proc in psutil.process_iter(['pid', 'name']):
            if app_name.lower() in proc.info['name'].lower():
                proc.terminate()
                logger.info(f"Closed {app_name}")
                return True
        return False
        
    async def list_running_apps(self) -> List[Dict]:
        apps = []
        for proc in psutil.process_iter(['pid', 'name', 'memory_percent', 'cpu_percent']):
            try:
                apps.append({
                    "pid": proc.info['pid'],
                    "name": proc.info['name'],
                    "memory": proc.info['memory_percent'],
                    "cpu": proc.info['cpu_percent']
                })
            except:
                continue
        return apps
        
    async def execute_script(self, script_path: str) -> str:
        result = subprocess.run(["python", script_path], capture_output=True, text=True)
        return result.stdout
        
    async def mouse_click(self, x: int = None, y: int = None, button: str = "left"):
        if x is None or y is None:
            x, y = pyautogui.position()
        pyautogui.click(x, y, button=button)
        
    async def mouse_move(self, x: int, y: int, duration: float = 0.2):
        pyautogui.moveTo(x, y, duration=duration)
        
    async def type_text(self, text: str):
        pyautogui.write(text)
        
    async def press_key(self, key: str):
        pyautogui.press(key)
        
    async def hotkey(self, *keys):
        pyautogui.hotkey(*keys)
        
    async def scroll(self, clicks: int):
        pyautogui.scroll(clicks)
        
    async def get_mouse_position(self) -> tuple:
        return pyautogui.position()
        
    async def take_screenshot(self, save_path: str = None) -> str:
        screenshot = pyautogui.screenshot()
        if save_path:
            screenshot.save(save_path)
            return save_path
        return screenshot