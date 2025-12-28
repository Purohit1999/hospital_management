from django.conf import settings
from django.db import models
from django.utils import timezone


class KnowledgeDocument(models.Model):
    name = models.CharField(max_length=255)
    path = models.CharField(max_length=500)
    checksum = models.CharField(max_length=64)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class AgentQueryLog(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )
    query = models.TextField()
    response = models.TextField(blank=True)
    latency_ms = models.IntegerField(default=0)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class AiDraft(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )
    patient_id = models.IntegerField(null=True, blank=True)
    notes = models.TextField()
    draft_text = models.TextField()
    patient_instructions = models.TextField(blank=True)
    reviewed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


class AppointmentRiskScore(models.Model):
    appointment_id = models.IntegerField()
    risk_score = models.FloatField()
    computed_at = models.DateTimeField(default=timezone.now)


class AiPredictionLog(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )
    input_text = models.TextField()
    predicted_label = models.CharField(max_length=100)
    confidence = models.FloatField(default=0.0)
    overridden_label = models.CharField(max_length=100, blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class AgentRun(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )
    run_type = models.CharField(max_length=100)
    status = models.CharField(max_length=20, default="success")
    total_latency_ms = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)


class AgentStepTrace(models.Model):
    run = models.ForeignKey(AgentRun, on_delete=models.CASCADE, related_name="steps")
    step_name = models.CharField(max_length=50)
    input_text = models.TextField(blank=True)
    output_text = models.TextField(blank=True)
    latency_ms = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
