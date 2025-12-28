import os
import time
import requests
from django.conf import settings


def _mock_response(prompt: str) -> str:
    return (
        "Mock response generated. Summary:\n"
        f"- Input length: {len(prompt)} characters\n"
        "- This is a placeholder output when no API key is configured."
    )


def generate_text(prompt: str, system: str = "") -> str:
    provider = getattr(settings, "LLM_PROVIDER", "mock")
    api_key = os.getenv("OPENAI_API_KEY", "")
    if provider == "mock" or not api_key:
        return _mock_response(prompt)

    start = time.time()
    url = "https://api.openai.com/v1/chat/completions"
    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": system or "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.2,
    }
    headers = {"Authorization": f"Bearer {api_key}"}
    response = requests.post(url, json=payload, headers=headers, timeout=30)
    response.raise_for_status()
    data = response.json()
    content = data["choices"][0]["message"]["content"]
    _ = int((time.time() - start) * 1000)
    return content
