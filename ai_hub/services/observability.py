import json
import os
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, Optional

from django.conf import settings

from ai_hub.models import AiRequestTrace


TRACE_FILE = os.path.join(settings.AI_HUB_ARTIFACTS_DIR, "ai_traces.jsonl")


def new_request_id() -> uuid.UUID:
    return uuid.uuid4()


def trace_success(
    *,
    request_id: uuid.UUID,
    user,
    route: str,
    operation_type: str,
    latency_ms: int,
    metadata: Optional[Dict[str, Any]] = None,
):
    _persist_trace(
        request_id=request_id,
        user=user,
        route=route,
        operation_type=operation_type,
        latency_ms=latency_ms,
        success=True,
        error_message="",
        metadata=metadata or {},
    )


def trace_error(
    *,
    request_id: uuid.UUID,
    user,
    route: str,
    operation_type: str,
    latency_ms: int,
    error_message: str,
    metadata: Optional[Dict[str, Any]] = None,
):
    _persist_trace(
        request_id=request_id,
        user=user,
        route=route,
        operation_type=operation_type,
        latency_ms=latency_ms,
        success=False,
        error_message=error_message,
        metadata=metadata or {},
    )


def _persist_trace(
    *,
    request_id: uuid.UUID,
    user,
    route: str,
    operation_type: str,
    latency_ms: int,
    success: bool,
    error_message: str,
    metadata: Dict[str, Any],
):
    trace = AiRequestTrace.objects.create(
        request_id=request_id,
        user=user if user and getattr(user, "is_authenticated", False) else None,
        route=route,
        operation_type=operation_type,
        llm_provider=getattr(settings, "LLM_PROVIDER", ""),
        rag_provider=getattr(settings, "RAG_PROVIDER", ""),
        latency_ms=latency_ms,
        success=success,
        error_message=error_message,
        metadata=metadata,
    )
    _write_jsonl(
        {
            "request_id": str(request_id),
            "user_id": trace.user_id,
            "route": route,
            "operation_type": operation_type,
            "llm_provider": trace.llm_provider,
            "rag_provider": trace.rag_provider,
            "latency_ms": latency_ms,
            "success": success,
            "error_message": error_message,
            "metadata": metadata,
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
    )


def _write_jsonl(payload: Dict[str, Any]) -> None:
    try:
        os.makedirs(settings.AI_HUB_ARTIFACTS_DIR, exist_ok=True)
        with open(TRACE_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(payload, ensure_ascii=True) + "\n")
    except Exception:
        pass
