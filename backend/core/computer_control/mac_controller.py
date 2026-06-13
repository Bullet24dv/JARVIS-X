import subprocess
import psutil
from typing import List, Dict

class MacController:
    async def open_app(self, app_name: str) -> bool:
        subprocess.run(["open", "-a", app_name])
        return True
        
    async def close_app(self, app_name: str) -> bool:
        subprocess.run(["osascript", "-e", f'tell application "{app_name}" to quit'])
        return True
        
    async def list_running_apps(self) -> List[Dict]:
        apps = []
        for proc in psutil.process_iter(['pid', 'name']):
            apps.append({"pid": proc.info['pid'], "name": proc.info['name']})
        return apps