import platform
from backend.core.computer_control.windows_controller import WindowsController
from backend.core.computer_control.linux_controller import LinuxController
from backend.core.computer_control.mac_controller import MacController
from loguru import logger

class ComputerService:
    def __init__(self):
        self.os_name = platform.system()
        if self.os_name == "Windows":
            self.controller = WindowsController()
        elif self.os_name == "Linux":
            self.controller = LinuxController()
        elif self.os_name == "Darwin":
            self.controller = MacController()
        else:
            self.controller = None
            logger.warning(f"Unsupported OS: {self.os_name}")
            
    async def open_app(self, app_name: str) -> bool:
        if self.controller:
            return await self.controller.open_app(app_name)
        return False
        
    async def close_app(self, app_name: str) -> bool:
        if self.controller:
            return await self.controller.close_app(app_name)
        return False
        
    async def list_running(self) -> list:
        if self.controller:
            return await self.controller.list_running_apps()
        return []
        
    async def execute_script(self, script_path: str) -> str:
        if self.controller:
            return await self.controller.execute_script(script_path)
        return ""
        
    async def mouse_click(self, x: int = None, y: int = None, button: str = "left"):
        if self.controller and hasattr(self.controller, 'mouse_click'):
            await self.controller.mouse_click(x, y, button)
            
    async def type_text(self, text: str):
        if self.controller and hasattr(self.controller, 'type_text'):
            await self.controller.type_text(text)