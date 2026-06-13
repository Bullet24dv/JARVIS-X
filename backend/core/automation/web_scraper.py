from playwright.async_api import Page
from bs4 import BeautifulSoup

class WebScraper:
    def __init__(self, page: Page):
        self.page = page
        
    async def get_html(self) -> str:
        return await self.page.content()
        
    async def get_text_by_selector(self, selector: str) -> str:
        elements = await self.page.query_selector_all(selector)
        texts = []
        for el in elements:
            text = await el.text_content()
            if text:
                texts.append(text.strip())
        return "\n".join(texts)
        
    async def get_links(self) -> list:
        links = await self.page.eval_on_selector_all("a", "elements => elements.map(el => el.href)")
        return links