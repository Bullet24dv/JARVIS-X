# ============================================================
# JARVIS-X | backend/core/llm_router.py
# Router de modelos IA con selección automática y fallback
# ============================================================

import asyncio
import logging
import time
from typing import Any, AsyncGenerator, Dict, List, Optional, Union
from dataclasses import dataclass, field
from enum import Enum

import httpx

from backend.config import settings

logger = logging.getLogger("jarvis.llm_router")


class LLMProvider(str, Enum):
    DEEPSEEK = "deepseek"
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GEMINI = "gemini"
    OLLAMA = "ollama"
    OPENROUTER = "openrouter"


@dataclass
class LLMMessage:
    role: str  # system | user | assistant
    content: str


@dataclass
class LLMResponse:
    content: str
    provider: str
    model: str
    tokens_used: int = 0
    latency_ms: float = 0.0
    cached: bool = False


@dataclass
class ProviderStatus:
    name: str
    available: bool = True
    last_error: Optional[str] = None
    last_check: float = 0.0
    error_count: int = 0
    total_requests: int = 0
    avg_latency_ms: float = 0.0


class LLMRouter:
    """
    Router inteligente de modelos IA.
    - Selección automática según disponibilidad y latencia
    - Fallback automático en caso de error
    - Caché de respuestas con Redis
    - Streaming compatible con todos los proveedores
    """

    def __init__(self):
        self._providers: Dict[str, ProviderStatus] = {}
        self._priority: List[str] = settings.LLM_PRIORITY
        self._http: Optional[httpx.AsyncClient] = None
        self._system_prompt: str = settings.JARVIS_PERSONA
        self._cache: Optional[Any] = None  # Redis client, inyectado después

    async def initialize(self):
        """Inicializa el router y valida proveedores disponibles."""
        self._http = httpx.AsyncClient(timeout=settings.LLM_TIMEOUT)

        for provider in LLMProvider:
            self._providers[provider.value] = ProviderStatus(name=provider.value)

        # Validar disponibilidad en paralelo
        checks = [self._check_provider(p) for p in self._priority]
        await asyncio.gather(*checks, return_exceptions=True)

        available = [p for p, s in self._providers.items() if s.available]
        logger.info(f"Proveedores disponibles: {available}")

        if not available:
            logger.warning("¡Ningún proveedor LLM disponible! Verifique sus API keys.")

    async def _check_provider(self, provider: str) -> bool:
        """Verifica si un proveedor está operativo."""
        try:
            status = self._providers.get(provider)
            if not status:
                return False

            if provider == LLMProvider.DEEPSEEK and settings.DEEPSEEK_API_KEY:
                # Ping rápido
                r = await self._http.get(
                    f"{settings.DEEPSEEK_BASE_URL}/models",
                    headers={"Authorization": f"Bearer {settings.DEEPSEEK_API_KEY}"},
                    timeout=5,
                )
                status.available = r.status_code == 200

            elif provider == LLMProvider.OPENAI and settings.OPENAI_API_KEY:
                r = await self._http.get(
                    "https://api.openai.com/v1/models",
                    headers={"Authorization": f"Bearer {settings.OPENAI_API_KEY}"},
                    timeout=5,
                )
                status.available = r.status_code == 200

            elif provider == LLMProvider.ANTHROPIC and settings.ANTHROPIC_API_KEY:
                status.available = True  # Anthropic no tiene endpoint de ping público

            elif provider == LLMProvider.GEMINI and settings.GEMINI_API_KEY:
                status.available = True

            elif provider == LLMProvider.OLLAMA and settings.OLLAMA_ENABLED:
                r = await self._http.get(f"{settings.OLLAMA_BASE_URL}/api/tags", timeout=3)
                status.available = r.status_code == 200

            elif provider == LLMProvider.OPENROUTER and settings.OPENROUTER_API_KEY:
                status.available = True

            else:
                status.available = False

            return status.available

        except Exception as e:
            self._providers[provider].available = False
            self._providers[provider].last_error = str(e)
            return False

    def get_status(self) -> Dict[str, Any]:
        """Retorna estado de todos los proveedores."""
        return {
            p: {
                "available": s.available,
                "requests": s.total_requests,
                "avg_latency_ms": round(s.avg_latency_ms, 2),
                "last_error": s.last_error,
            }
            for p, s in self._providers.items()
        }

    def _get_available_providers(self) -> List[str]:
        """Retorna proveedores disponibles en orden de prioridad."""
        return [p for p in self._priority if self._providers.get(p, ProviderStatus(p)).available]

    async def chat(
        self,
        messages: List[LLMMessage],
        provider: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2048,
        system_override: Optional[str] = None,
        stream: bool = False,
    ) -> LLMResponse:
        """
        Envía mensajes al LLM con fallback automático.
        Si `provider` es None, usa el primero disponible en la cadena de prioridad.
        """
        providers_to_try = [provider] if provider else self._get_available_providers()

        if not providers_to_try:
            raise RuntimeError("Ningún proveedor LLM disponible. Verifique su conexión y API keys.")

        system = system_override or self._system_prompt
        last_error = None

        for p in providers_to_try:
            try:
                start = time.perf_counter()
                response = await self._call_provider(
                    provider=p,
                    messages=messages,
                    system=system,
                    temperature=temperature,
                    max_tokens=max_tokens,
                )
                elapsed = (time.perf_counter() - start) * 1000
                response.latency_ms = elapsed

                # Actualizar estadísticas
                status = self._providers[p]
                status.total_requests += 1
                status.avg_latency_ms = (
                    (status.avg_latency_ms * (status.total_requests - 1) + elapsed)
                    / status.total_requests
                )
                status.error_count = 0  # reset on success

                logger.debug(f"[{p}] Respuesta en {elapsed:.0f}ms ({response.tokens_used} tokens)")
                return response

            except Exception as e:
                last_error = e
                logger.warning(f"Proveedor '{p}' falló: {e}. Intentando siguiente...")
                self._providers[p].error_count += 1
                self._providers[p].last_error = str(e)
                if self._providers[p].error_count >= 3:
                    self._providers[p].available = False
                    logger.error(f"Proveedor '{p}' marcado como no disponible.")
                continue

        raise RuntimeError(f"Todos los proveedores fallaron. Último error: {last_error}")

    async def _call_provider(
        self,
        provider: str,
        messages: List[LLMMessage],
        system: str,
        temperature: float,
        max_tokens: int,
    ) -> LLMResponse:
        """Despacha la llamada al proveedor específico."""
        dispatch = {
            LLMProvider.DEEPSEEK: self._call_deepseek,
            LLMProvider.OPENAI: self._call_openai,
            LLMProvider.ANTHROPIC: self._call_anthropic,
            LLMProvider.GEMINI: self._call_gemini,
            LLMProvider.OLLAMA: self._call_ollama,
            LLMProvider.OPENROUTER: self._call_openrouter,
        }
        fn = dispatch.get(provider)
        if not fn:
            raise ValueError(f"Proveedor desconocido: {provider}")
        return await fn(messages=messages, system=system, temperature=temperature, max_tokens=max_tokens)

    # ── DeepSeek ─────────────────────────────────────────────
    async def _call_deepseek(self, messages, system, temperature, max_tokens) -> LLMResponse:
        payload = {
            "model": settings.DEEPSEEK_MODEL,
            "messages": [{"role": "system", "content": system}]
            + [{"role": m.role, "content": m.content} for m in messages],
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        r = await self._http.post(
            f"{settings.DEEPSEEK_BASE_URL}/chat/completions",
            json=payload,
            headers={"Authorization": f"Bearer {settings.DEEPSEEK_API_KEY}"},
        )
        r.raise_for_status()
        data = r.json()
        return LLMResponse(
            content=data["choices"][0]["message"]["content"],
            provider="deepseek",
            model=settings.DEEPSEEK_MODEL,
            tokens_used=data.get("usage", {}).get("total_tokens", 0),
        )

    # ── OpenAI ───────────────────────────────────────────────
    async def _call_openai(self, messages, system, temperature, max_tokens) -> LLMResponse:
        payload = {
            "model": settings.OPENAI_MODEL,
            "messages": [{"role": "system", "content": system}]
            + [{"role": m.role, "content": m.content} for m in messages],
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        r = await self._http.post(
            "https://api.openai.com/v1/chat/completions",
            json=payload,
            headers={"Authorization": f"Bearer {settings.OPENAI_API_KEY}"},
        )
        r.raise_for_status()
        data = r.json()
        return LLMResponse(
            content=data["choices"][0]["message"]["content"],
            provider="openai",
            model=settings.OPENAI_MODEL,
            tokens_used=data.get("usage", {}).get("total_tokens", 0),
        )

    # ── Anthropic ────────────────────────────────────────────
    async def _call_anthropic(self, messages, system, temperature, max_tokens) -> LLMResponse:
        payload = {
            "model": settings.ANTHROPIC_MODEL,
            "max_tokens": max_tokens,
            "system": system,
            "messages": [{"role": m.role, "content": m.content} for m in messages],
        }
        r = await self._http.post(
            "https://api.anthropic.com/v1/messages",
            json=payload,
            headers={
                "x-api-key": settings.ANTHROPIC_API_KEY,
                "anthropic-version": "2023-06-01",
            },
        )
        r.raise_for_status()
        data = r.json()
        return LLMResponse(
            content=data["content"][0]["text"],
            provider="anthropic",
            model=settings.ANTHROPIC_MODEL,
            tokens_used=data.get("usage", {}).get("input_tokens", 0)
            + data.get("usage", {}).get("output_tokens", 0),
        )

    # ── Gemini ───────────────────────────────────────────────
    async def _call_gemini(self, messages, system, temperature, max_tokens) -> LLMResponse:
        contents = [{"role": "model" if m.role == "assistant" else "user", "parts": [{"text": m.content}]}
                    for m in messages]
        payload = {
            "system_instruction": {"parts": [{"text": system}]},
            "contents": contents,
            "generationConfig": {"temperature": temperature, "maxOutputTokens": max_tokens},
        }
        url = (f"https://generativelanguage.googleapis.com/v1beta/models/"
               f"{settings.GEMINI_MODEL}:generateContent?key={settings.GEMINI_API_KEY}")
        r = await self._http.post(url, json=payload)
        r.raise_for_status()
        data = r.json()
        text = data["candidates"][0]["content"]["parts"][0]["text"]
        return LLMResponse(
            content=text,
            provider="gemini",
            model=settings.GEMINI_MODEL,
            tokens_used=data.get("usageMetadata", {}).get("totalTokenCount", 0),
        )

    # ── Ollama ───────────────────────────────────────────────
    async def _call_ollama(self, messages, system, temperature, max_tokens) -> LLMResponse:
        payload = {
            "model": settings.OLLAMA_MODEL,
            "messages": [{"role": "system", "content": system}]
            + [{"role": m.role, "content": m.content} for m in messages],
            "stream": False,
            "options": {"temperature": temperature, "num_predict": max_tokens},
        }
        r = await self._http.post(
            f"{settings.OLLAMA_BASE_URL}/api/chat",
            json=payload,
            timeout=60,
        )
        r.raise_for_status()
        data = r.json()
        return LLMResponse(
            content=data["message"]["content"],
            provider="ollama",
            model=settings.OLLAMA_MODEL,
            tokens_used=data.get("eval_count", 0),
        )

    # ── OpenRouter ───────────────────────────────────────────
    async def _call_openrouter(self, messages, system, temperature, max_tokens) -> LLMResponse:
        payload = {
            "model": settings.OPENROUTER_MODEL,
            "messages": [{"role": "system", "content": system}]
            + [{"role": m.role, "content": m.content} for m in messages],
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        r = await self._http.post(
            f"{settings.OPENROUTER_BASE_URL}/chat/completions",
            json=payload,
            headers={
                "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
                "HTTP-Referer": "https://jarvis-x.local",
                "X-Title": "JARVIS-X",
            },
        )
        r.raise_for_status()
        data = r.json()
        return LLMResponse(
            content=data["choices"][0]["message"]["content"],
            provider="openrouter",
            model=settings.OPENROUTER_MODEL,
            tokens_used=data.get("usage", {}).get("total_tokens", 0),
        )

    # ── Streaming ────────────────────────────────────────────
    async def stream(
        self,
        messages: List[LLMMessage],
        provider: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2048,
        system_override: Optional[str] = None,
    ) -> AsyncGenerator[str, None]:
        """Stream de tokens en tiempo real (proveedor activo o DeepSeek por defecto)."""
        p = provider or self._get_available_providers()[0]
        system = system_override or self._system_prompt

        if p == LLMProvider.DEEPSEEK:
            async for chunk in self._stream_openai_compatible(
                url=f"{settings.DEEPSEEK_BASE_URL}/chat/completions",
                key=settings.DEEPSEEK_API_KEY,
                model=settings.DEEPSEEK_MODEL,
                messages=messages,
                system=system,
                temperature=temperature,
                max_tokens=max_tokens,
            ):
                yield chunk

        elif p == LLMProvider.OPENAI:
            async for chunk in self._stream_openai_compatible(
                url="https://api.openai.com/v1/chat/completions",
                key=settings.OPENAI_API_KEY,
                model=settings.OPENAI_MODEL,
                messages=messages,
                system=system,
                temperature=temperature,
                max_tokens=max_tokens,
            ):
                yield chunk
        else:
            # Fallback: llamada normal
            resp = await self.chat(messages, provider=p, temperature=temperature,
                                   max_tokens=max_tokens, system_override=system_override)
            yield resp.content

    async def _stream_openai_compatible(
        self, url: str, key: str, model: str,
        messages: List[LLMMessage], system: str,
        temperature: float, max_tokens: int,
    ) -> AsyncGenerator[str, None]:
        """Streaming compatible con API OpenAI."""
        payload = {
            "model": model,
            "messages": [{"role": "system", "content": system}]
            + [{"role": m.role, "content": m.content} for m in messages],
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": True,
        }
        async with self._http.stream(
            "POST", url,
            json=payload,
            headers={"Authorization": f"Bearer {key}"},
        ) as r:
            r.raise_for_status()
            async for line in r.aiter_lines():
                if line.startswith("data: "):
                    data = line[6:]
                    if data == "[DONE]":
                        break
                    try:
                        import json
                        chunk = json.loads(data)
                        delta = chunk["choices"][0].get("delta", {}).get("content", "")
                        if delta:
                            yield delta
                    except Exception:
                        continue

    async def shutdown(self):
        if self._http:
            await self._http.aclose()