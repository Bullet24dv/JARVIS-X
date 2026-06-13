import pyautogui
import asyncio

class InputController:
    @staticmethod
    async def click(x: int, y: int, button: str = "left", clicks: int = 1):
        pyautogui.click(x, y, button=button, clicks=clicks)
        
    @staticmethod
    async def double_click(x: int, y: int):
        pyautogui.doubleClick(x, y)
        
    @staticmethod
    async def right_click(x: int, y: int):
        pyautogui.rightClick(x, y)
        
    @staticmethod
    async def drag(start_x: int, start_y: int, end_x: int, end_y: int, duration: float = 0.5):
        pyautogui.moveTo(start_x, start_y)
        pyautogui.drag(end_x - start_x, end_y - start_y, duration=duration)
        
    @staticmethod
    async def type_with_delay(text: str, delay: float = 0.05):
        for char in text:
            pyautogui.write(char)
            await asyncio.sleep(delay)