import logging

from .services.llm import generate_text

logger = logging.getLogger(__name__)


def _redact_pii(text: str) -> str:
    if not text:
        return text
    import re

    text = re.sub(r"\b[\w\.-]+@[\w\.-]+\.\w+\b", "[REDACTED_EMAIL]", text)
    text = re.sub(r"\b\d{10,12}\b", "[REDACTED_NUMBER]", text)
    return text


def generate_draft_job(notes: str, redact: bool) -> dict:
    notes = (notes or "").strip()
    if len(notes) > 4000:
        notes = notes[:4000]
    safe_notes = _redact_pii(notes) if redact else notes
    prompt = (
        "Draft a discharge summary and patient-friendly instructions.\n\n"
        f"Notes:\n{safe_notes}\n"
    )
    response = generate_text(prompt, max_tokens=256, timeout=20)
    parts = response.split("\n\n", 1)
    draft = parts[0]
    instructions = parts[1] if len(parts) > 1 else ""
    return {"draft": draft, "instructions": instructions}
