import time
from typing import Dict, List

from .rag import retrieve
from .llm import generate_text


def run_compliance_agent(draft_text: str, use_llm: bool = True) -> Dict:
    start = time.time()
    steps = []

    plan = [
        "Check required sections (diagnosis, treatment, medications, follow-up).",
        "Check safety language and red flags.",
        "Check patient-friendly instructions.",
        "Check provider sign-off.",
    ]
    steps.append({"step": "PLAN", "output": "\n".join(plan)})

    retrieval_query = (
        "discharge summary SOP required sections medication list follow-up "
        "red flags sign-off privacy clinician review"
    )
    citations, _ = retrieve(retrieval_query, top_k=3)
    cite_text = "\n".join(
        [f"- {c['source']}: {c['snippet']}" for c in citations]
    )
    steps.append({"step": "RETRIEVE", "output": cite_text or "No citations found."})

    checklist = [
        "Diagnosis present: " + ("yes" if "diagnos" in draft_text.lower() else "no"),
        "Follow-up present: " + ("yes" if "follow" in draft_text.lower() else "no"),
        "Medication list present: " + ("yes" if "med" in draft_text.lower() else "no"),
    ]
    steps.append({"step": "VALIDATE", "output": "\n".join(checklist)})

    report_prompt = (
        "Review the discharge summary for policy compliance. "
        "List issues with severity and suggest edits.\n\n"
        f"Summary:\n{draft_text}\n"
        f"Policy snippets:\n{cite_text}\n"
    )
    report = generate_text(report_prompt) if use_llm else "Mock compliance report."
    steps.append({"step": "REPORT", "output": report})

    total_latency_ms = int((time.time() - start) * 1000)
    return {
        "steps": steps,
        "latency_ms": total_latency_ms,
        "citations": citations,
    }
