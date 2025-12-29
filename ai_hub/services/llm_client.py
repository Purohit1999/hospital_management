import logging
import time
from typing import Optional

import requests
from django.conf import settings

logger = logging.getLogger(__name__)


def generate_answer(prompt: str, model: str, provider: str) -> str:
    if getattr(settings, "AI_MOCK_MODE", False):
        return _mock_response(prompt)

    provider = (provider or "openai").strip().lower()
    if provider == "openai":
        api_key = getattr(settings, "OPENAI_API_KEY", "")
        if not api_key:
            logger.error("OpenAI API key missing. Set OPENAI_API_KEY.")
            raise ValueError("LLM is not configured. Set OPENAI_API_KEY and redeploy.")
        return _openai_answer(prompt, model, api_key)

    if provider == "anthropic":
        api_key = getattr(settings, "ANTHROPIC_API_KEY", "")
        if not api_key:
            logger.error("Anthropic API key missing. Set ANTHROPIC_API_KEY.")
            raise ValueError("LLM is not configured. Set ANTHROPIC_API_KEY and redeploy.")
        return _anthropic_answer(prompt, model, api_key)

    logger.error("Unsupported LLM_PROVIDER=%s", provider)
    raise ValueError("LLM provider is not supported. Set LLM_PROVIDER correctly.")


def _mock_response(prompt: str) -> str:
    return (
        "Mock response generated. Summary:\n"
        f"- Input length: {len(prompt)} characters\n"
        "- This is a placeholder output in mock mode."
    )


def _openai_answer(prompt: str, model: str, api_key: str) -> str:
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        return _openai_sdk_call(client, prompt, model)
    except Exception:
        return _openai_http_call(prompt, model, api_key)


def _openai_sdk_call(client, prompt: str, model: str) -> str:
    response = _retry(
        lambda: client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": _system_instructions()},
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
        )
    )
    return response.choices[0].message.content


def _openai_http_call(prompt: str, model: str, api_key: str) -> str:
    url = "https://api.openai.com/v1/chat/completions"
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": _system_instructions()},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.2,
    }
    headers = {"Authorization": f"Bearer {api_key}"}
    response = _retry(
        lambda: requests.post(url, json=payload, headers=headers, timeout=30)
    )
    response.raise_for_status()
    data = response.json()
    return data["choices"][0]["message"]["content"]


def _anthropic_answer(prompt: str, model: str, api_key: str) -> str:
    url = "https://api.anthropic.com/v1/messages"
    payload = {
        "model": model or "claude-3-5-sonnet-20240620",
        "max_tokens": 512,
        "system": _system_instructions(),
        "messages": [{"role": "user", "content": prompt}],
    }
    headers = {
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json",
    }
    response = _retry(
        lambda: requests.post(url, json=payload, headers=headers, timeout=30)
    )
    response.raise_for_status()
    data = response.json()
    content = data.get("content", [])
    if content:
        return content[0].get("text", "")
    return ""


def _retry(callable_fn):
    last_exc: Optional[Exception] = None
    for _ in range(2):
        try:
            return callable_fn()
        except requests.RequestException as exc:
            last_exc = exc
            time.sleep(0.5)
    if last_exc:
        raise last_exc
    return callable_fn()


def _system_instructions() -> str:
    return (
        "You are a clinical assistant. Use only the provided context. "
        "Do not invent facts. If unsure, say you do not know."
    )
