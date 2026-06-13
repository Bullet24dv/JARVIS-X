from playwright.async_api import async_playwright, Browser, Page
from contextlib import asynccontextmanager

class PlaywrightManager:
    def __init__(self):
        self.playwright = None
        self.browser = None
        
    async def __aenter__(self):
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=False)
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.browser.close()
        await self.playwright.stop()
        
    async def new_page(self) -> Page:
        return await self.browser.new_page()