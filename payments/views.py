from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import Payment


@login_required
def payment_success_view(request):
    last_payment = (
        Payment.objects.filter(user=request.user, status="pending")
        .order_by("-created_at")
        .first()
    )
    if last_payment:
        last_payment.status = "succeeded"
        last_payment.save(update_fields=["status"])
    return render(request, "payments/success.html")
