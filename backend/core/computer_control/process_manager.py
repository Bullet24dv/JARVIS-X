import psutil
import signal
from typing import Optional

class ProcessManager:
    @staticmethod
    def get_process_by_name(name: str) -> Optional[psutil.Process]:
        for proc in psutil.process_iter(['pid', 'name']):
            if name.lower() in proc.info['name'].lower():
                return proc
        return None
        
    @staticmethod
    def kill_process(pid: int):
        try:
            proc = psutil.Process(pid)
            proc.terminate()
        except:
            pass
            
    @staticmethod
    def get_system_stats() -> dict:
        return {
            "cpu_percent": psutil.cpu_percent(interval=1),
            "memory_percent": psutil.virtual_memory().percent,
            "disk_usage": psutil.disk_usage('/').percent
        }