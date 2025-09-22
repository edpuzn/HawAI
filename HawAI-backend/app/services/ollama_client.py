from __future__ import annotations
import httpx
from typing import AsyncGenerator, Dict, Any
from app.core.config import settings


class OllamaClient:
    def __init__(self, base_url: str | None = None, model: str | None = None):
        self.base_url = (base_url or settings.ollama_host).rstrip("/")
        self.model = model or settings.model_name
        # Increase timeout for multimodal generation (LLaVA may take longer)
        self._client = httpx.AsyncClient(base_url=self.base_url, timeout=120)

    async def ping(self) -> bool:
        try:
            async with httpx.AsyncClient(base_url=self.base_url, timeout=10) as ac:
                resp = await ac.get("/api/tags")
                if resp.status_code != 200:
                    return False
                _ = resp.json()
                return True
        except Exception:
            return False

    async def generate(self, prompt: str, user_meta: Dict[str, Any] | None = None, image_url: str | None = None, image_base64: str | None = None) -> str:
        # Use role-based chat API so Modelfile SYSTEM ve şablonları daha iyi uygulanır
        messages: list[dict[str, str]] = []
        if settings.system_prompt:
            messages.append({"role": "system", "content": settings.system_prompt})
        messages.append({"role": "user", "content": prompt})

        payload = {
            "model": self.model,
            "messages": messages,
            "stream": False,
            "options": {
                "temperature": 0.2,
            },
        }
        if image_url or image_base64:
            images: list[str] = []
            if image_url:
                images.append(image_url)
            if image_base64:
                images.append(image_base64)
            # LLaVA, Ollama chat API'de kullanıcı mesajına images alanı ile sağlanır
            payload["messages"][-1]["images"] = images
        if user_meta:
            payload["metadata"] = user_meta
        resp = await self._client.post("/api/chat", json=payload)
        resp.raise_for_status()
        data = resp.json()
        # Ollama /api/chat döndürdüğü yapı: { message: { role, content }, ... }
        message = data.get("message") or {}
        return message.get("content", "")

    async def chat_messages(
        self,
        messages: list[dict[str, str]],
        temperature: float = 0.2,
        images: list[str] | None = None,
    ) -> str:
        payload = {
            "model": self.model,
            "messages": messages,
            "stream": False,
            "options": {
                "temperature": temperature,
            },
        }
        if images:
            # Ollama LLaVA: images list is on the last user message
            try:
                if payload["messages"] and payload["messages"][-1].get("role") == "user":
                    payload["messages"][-1]["images"] = images
            except Exception:
                pass
        resp = await self._client.post("/api/chat", json=payload)
        resp.raise_for_status()
        data = resp.json()
        message = data.get("message") or {}
        return message.get("content", "")

    async def aclose(self) -> None:
        await self._client.aclose()

    async def __aenter__(self) -> "OllamaClient":
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        await self.aclose()
