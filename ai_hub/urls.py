from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="ai-dashboard"),
    path("rag/", views.rag_qa, name="ai-rag"),
    path("rag/upload/", views.rag_upload, name="ai-rag-upload"),
    path("draft/", views.draft_assistant, name="ai-draft"),
    path("agent/compliance/", views.compliance_agent, name="ai-agent-compliance"),
    path("ml/no-show/", views.no_show_risk, name="ai-no-show"),
    path("nlp/triage/", views.complaint_classifier, name="ai-triage"),
    path("eval/", views.eval_dashboard, name="ai-eval"),
]
