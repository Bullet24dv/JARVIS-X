from playwright.async_api import async_playwright
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import asyncio
from loguru import logger

class BrowserAutomation:
    def __init__(self, use_playwright: bool = True):
        self.use_playwright = use_playwright
        self.playwright = None
        self.browser = None
        self.page = None
        self.driver = None
        
    async def start(self):
        if self.use_playwright:
            self.playwright = await async_playwright().start()
            self.browser = await self.playwright.chromium.launch(headless=False)
            self.page = await self.browser.new_page()
        else:
            options = webdriver.ChromeOptions()
            options.add_argument("--start-maximized")
            self.driver = webdriver.Chrome(options=options)
        logger.info("Browser automation started")
        
    async def goto(self, url: str):
        if self.use_playwright:
            await self.page.goto(url)
        else:
            self.driver.get(url)
            
    async def fill(self, selector: str, value: str):
        if self.use_playwright:
            await self.page.fill(selector, value)
        else:
            element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
            element.send_keys(value)
            
    async def click(self, selector: str):
        if self.use_playwright:
            await self.page.click(selector)
        else:
            element = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
            element.click()
            
    async def screenshot(self, path: str = "screenshot.png"):
        if self.use_playwright:
            await self.page.screenshot(path=path)
        else:
            self.driver.save_screenshot(path)
        return path
        
    async def close(self):
        if self.use_playwright:
            await self.browser.close()
            await self.playwright.stop()
        else:
            self.driver.quit()