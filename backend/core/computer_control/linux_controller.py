import subprocess
import psutil
import asyncio
from typing import List, Dict
from loguru import logger

class LinuxController:
    async def open_app(self, app_name: str) -> bool:
        try:
            subprocess.Popen([app_name], shell=False)
            return True
        except Exception:
            try:
                subprocess.Popen(["xdg-open", app_name], shell=False)
                return True
            except Exception as e:
                logger.error(f"Failed to open {app_name}: {e}")
                return False
                
    async def close_app(self, app_name: str) -> bool:
        try:
            subprocess.run(["pkill", app_name])
            return True
        except:
            return False
            
    async def list_running_apps(self) -> List[Dict]:
        apps = []
        for proc in psutil.process_iter(['pid', 'name', 'memory_percent']):
            apps.append({
                "pid": proc.info['pid'],
                "name": proc.info['name'],
                "memory": proc.info['memory_percent']
            })
        return apps
        
    async def execute_script(self, script_path: str) -> str:
        result = subprocess.run(["python3", script_path], capture_output=True, text=True)
        return result.stdout