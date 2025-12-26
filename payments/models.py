from django.conf import settings
from django.db import models


class Payment(models.Model):
    STATUS_CHOICES = [
        ("created", "Created"),
        ("pending", "Pending"),
        ("paid", "Paid"),
        ("failed", "Failed"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="payments",
    )
    patient = models.ForeignKey(
        "hospital.Patient",
        on_delete=models.CASCADE,
        related_name="payments",
        null=True,
        blank=True,
    )
    discharge = models.ForeignKey(
        "hospital.DischargeDetails",
        on_delete=models.SET_NULL,
        related_name="payments",
        null=True,
        blank=True,
    )
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    currency = models.CharField(max_length=10, default="gbp")
    stripe_session_id = models.CharField(max_length=255, blank=True)
    stripe_payment_intent = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="created")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.amount} {self.status}"
