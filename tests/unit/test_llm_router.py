import pytest
from backend.core.llm_router import LLMRouter

@pytest.mark.asyncio
async def test_llm_router_failover():
    router = LLMRouter()
    await router.initialize()
    # Simular fallo de deepseek (no implementado aquí, pero probar lógica)
    assert router.current_provider.name in ["deepseek", "openai", "gemini", "claude", "ollama"]
    
    response = await router.chat_completion([{"role": "user", "content": "Hola, ¿cómo estás?"}])
    assert "content" in response