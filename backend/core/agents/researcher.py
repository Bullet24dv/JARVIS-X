import aiohttp
from bs4 import BeautifulSoup
from typing import Dict, Any, List
from loguru import logger
from .base_agent import BaseAgent

class ResearcherAgent(BaseAgent):
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        query = input_data.get("query")
        if not query:
            return {"error": "No query provided"}
        return await self.research(query)
        
    async def research(self, query: str) -> Dict:
        # Buscar en web usando diferentes fuentes
        results = []
        # Google (simulado con scraping o serpapi)
        async with aiohttp.ClientSession() as session:
            url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
            headers = {"User-Agent": "Mozilla/5.0"}
            async with session.get(url, headers=headers) as resp:
                html = await resp.text()
                soup = BeautifulSoup(html, "html.parser")
                for g in soup.find_all("div", class_="g")[:5]:
                    title = g.find("h3")
                    link = g.find("a")
                    if title and link:
                        results.append({
                            "title": title.text,
                            "url": link.get("href")
                        })
        # Resumir usando LLM
        summary_prompt = f"Resume la siguiente información de búsqueda para '{query}':\n" + "\n".join([r["title"] for r in results])
        summary = await self.think(summary_prompt)
        return {"query": query, "results": results, "summary": summary}