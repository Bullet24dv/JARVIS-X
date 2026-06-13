from playwright.async_api import Page
from typing import Dict

class FormFiller:
    def __init__(self, page: Page):
        self.page = page
        
    async def fill_form(self, fields: Dict[str, str]):
        for selector, value in fields.items():
            await self.page.fill(selector, value)
            
    async def select_option(self, selector: str, value: str):
        await self.page.select_option(selector, value)
        
    async def check_checkbox(self, selector: str):
        await self.page.check(selector)