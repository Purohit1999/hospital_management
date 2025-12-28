import os
import time
import re
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect

from .models import KnowledgeDocument, AgentQueryLog, AiDraft, AppointmentRiskScore, AiPredictionLog, AgentRun, AgentStepTrace
from .services.rag import load_docs_from_dir, build_index, retrieve
from .services.llm import generate_text
from .services.ml import predict_no_show, predict_department
from .services.agent import run_compliance_agent


def _ai_enabled():
    return getattr(settings, "AI_FEATURES_ENABLED", False)


def _agents_enabled():
    return getattr(settings, "AGENTS_ENABLED", False)


def _rate_limit_ok(request, limit=10, window_seconds=60):
    now = int(time.time())
    key = "ai_hub_rate"
    data = request.session.get(key, {"ts": now, "count": 0})
    if now - data["ts"] > window_seconds:
        data = {"ts": now, "count": 0}
    data["count"] += 1
    request.session[key] = data
    return data["count"] <= limit


def _redact_pii(text: str) -> str:
    if not text:
        return text
    text = re.sub(r"\b[\w\.-]+@[\w\.-]+\.\w+\b", "[REDACTED_EMAIL]", text)
    text = re.sub(r"\b\d{10,12}\b", "[REDACTED_NUMBER]", text)
    return text


def dashboard(request):
    if not _ai_enabled():
        return render(request, "ai_hub/disabled.html")
    return render(request, "ai_hub/dashboard.html")


def rag_qa(request):
    if not _ai_enabled():
        return render(request, "ai_hub/disabled.html")

    answer = ""
    citations = []
    query = ""
    if request.method == "POST":
        if not _rate_limit_ok(request):
            messages.error(request, "Rate limit exceeded. Please wait and try again.")
            return redirect("ai-rag")
        query = request.POST.get("query", "")
        safe_query = _redact_pii(query) if request.POST.get("redact") else query
        citations, latency_ms = retrieve(safe_query, top_k=3)
        prompt = (
            "Answer the question using the provided policy snippets. "
            "Include brief citations.\n\n"
            f"Question: {safe_query}\n"
            f"Snippets: {citations}\n"
        )
        answer = generate_text(prompt)
        AgentQueryLog.objects.create(
            user=request.user if request.user.is_authenticated else None,
            query=query,
            response=answer,
            latency_ms=latency_ms,
            metadata={"citations": citations},
        )
    return render(
        request,
        "ai_hub/rag_qa.html",
        {"answer": answer, "citations": citations, "query": query},
    )


def rag_upload(request):
    if not _ai_enabled():
        return render(request, "ai_hub/disabled.html")
    if request.method == "POST":
        if not _rate_limit_ok(request):
            messages.error(request, "Rate limit exceeded. Please wait and try again.")
            return redirect("ai-rag-upload")
        file = request.FILES.get("file")
        if not file:
            messages.error(request, "Please select a file to upload.")
            return redirect("ai-rag-upload")
        storage = FileSystemStorage(location=settings.AI_HUB_KB_DIR)
        filename = storage.save(file.name, file)
        path = storage.path(filename)
        KnowledgeDocument.objects.get_or_create(
            name=filename, path=path, defaults={"checksum": "pending"}
        )
        messages.success(request, "Document uploaded. Run build_rag_index.")
    return render(request, "ai_hub/rag_upload.html")


def draft_assistant(request):
    if not _ai_enabled():
        return render(request, "ai_hub/disabled.html")

    draft = ""
    instructions = ""
    if request.method == "POST":
        if not _rate_limit_ok(request):
            messages.error(request, "Rate limit exceeded. Please wait and try again.")
            return redirect("ai-draft")
        notes = request.POST.get("notes", "")
        redact = request.POST.get("redact") == "on"
        safe_notes = _redact_pii(notes) if redact else notes
        prompt = (
            "Draft a discharge summary and patient-friendly instructions.\n\n"
            f"Notes:\n{safe_notes}\n"
        )
        response = generate_text(prompt)
        parts = response.split("\n\n", 1)
        draft = parts[0]
        instructions = parts[1] if len(parts) > 1 else ""
        if request.POST.get("reviewed") == "on":
            AiDraft.objects.create(
                user=request.user if request.user.is_authenticated else None,
                patient_id=request.POST.get("patient_id") or None,
                notes=notes,
                draft_text=draft,
                patient_instructions=instructions,
                reviewed=True,
            )
            messages.success(request, "Draft saved.")
    return render(
        request,
        "ai_hub/draft_assistant.html",
        {"draft": draft, "instructions": instructions},
    )


def compliance_agent(request):
    if not _ai_enabled() or not _agents_enabled():
        return render(request, "ai_hub/disabled.html")

    trace = []
    report = ""
    if request.method == "POST":
        if not _rate_limit_ok(request):
            messages.error(request, "Rate limit exceeded. Please wait and try again.")
            return redirect("ai-agent-compliance")
        text = request.POST.get("text", "")
        redact = request.POST.get("redact") == "on"
        safe_text = _redact_pii(text) if redact else text
        result = run_compliance_agent(safe_text, use_llm=True)
        trace = result["steps"]
        report = trace[-1]["output"] if trace else ""
        run = AgentRun.objects.create(
            user=request.user if request.user.is_authenticated else None,
            run_type="policy_compliance",
            status="success",
            total_latency_ms=result["latency_ms"],
        )
        for step in trace:
            AgentStepTrace.objects.create(
                run=run,
                step_name=step["step"],
                input_text=safe_text,
                output_text=step["output"],
                latency_ms=0,
            )
    return render(
        request,
        "ai_hub/agent_compliance.html",
        {"trace": trace, "report": report},
    )


def no_show_risk(request):
    if not _ai_enabled():
        return render(request, "ai_hub/disabled.html")
    scores = []
    if request.method == "POST":
        if not _rate_limit_ok(request):
            messages.error(request, "Rate limit exceeded. Please wait and try again.")
            return redirect("ai-no-show")
        days_until = int(request.POST.get("days_until", "2") or 2)
        hour = int(request.POST.get("hour", "9") or 9)
        score = predict_no_show({"days_until": days_until, "hour": hour})
        scores.append({"appointment_id": "demo", "risk": score})
    return render(request, "ai_hub/no_show.html", {"scores": scores})


def complaint_classifier(request):
    if not _ai_enabled():
        return render(request, "ai_hub/disabled.html")
    prediction = None
    if request.method == "POST":
        if not _rate_limit_ok(request):
            messages.error(request, "Rate limit exceeded. Please wait and try again.")
            return redirect("ai-triage")
        text = request.POST.get("complaint", "")
        pred, conf = predict_department(text)
        override = request.POST.get("override", "")
        AiPredictionLog.objects.create(
            user=request.user if request.user.is_authenticated else None,
            input_text=text,
            predicted_label=pred,
            confidence=conf,
            overridden_label=override,
            metadata={},
        )
        prediction = {"label": override or pred, "confidence": conf}
    return render(
        request,
        "ai_hub/complaint_classifier.html",
        {"prediction": prediction},
    )
