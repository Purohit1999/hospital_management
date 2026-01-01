from decimal import Decimal

import stripe
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

from hospital.models import DischargeDetails
from .models import Payment


def is_patient(user):
    return user.groups.filter(name="PATIENT").exists()


@login_required
@user_passes_test(is_patient)
def create_checkout_session(request, discharge_id):
    if request.method != "POST":
        messages.error(request, "Please use the Pay Bill button to start payment.")
        return redirect("patient-discharge-summary")

    discharge = get_object_or_404(
        DischargeDetails, pk=discharge_id, patient__user=request.user
    )

    if discharge.is_paid:
        messages.info(request, "This bill is already paid.")
        return redirect("patient-discharge-summary")

    if not settings.STRIPE_SECRET_KEY:
        messages.error(request, "Stripe is not configured. Please contact support.")
        return redirect("patient-discharge-summary")

    stripe.api_key = settings.STRIPE_SECRET_KEY
    amount_pence = int(Decimal(discharge.total) * 100)
    if amount_pence <= 0:
        messages.error(request, "Invalid payment amount.")
        return redirect("patient-discharge-summary")

    payment = Payment.objects.create(
        user=request.user,
        patient=discharge.patient,
        discharge=discharge,
        amount=discharge.total,
        currency=settings.STRIPE_CURRENCY,
        status="pending",
    )

    success_url = request.build_absolute_uri(
        reverse("payment-success")
    ) + "?session_id={CHECKOUT_SESSION_ID}"
    cancel_url = request.build_absolute_uri(reverse("payment-cancel"))

    session = stripe.checkout.Session.create(
        mode="payment",
        payment_method_types=["card"],
        line_items=[
            {
                "price_data": {
                    "currency": settings.STRIPE_CURRENCY,
                    "unit_amount": amount_pence,
                    "product_data": {
                        "name": "Hospital discharge bill",
                        "description": f"Discharge summary #{discharge.id}",
                    },
                },
                "quantity": 1,
            }
        ],
        success_url=success_url,
        cancel_url=cancel_url,
        customer_email=request.user.email or None,
        metadata={"discharge_id": str(discharge.id)},
    )

    payment.stripe_session_id = session.id
    payment.save(update_fields=["stripe_session_id"])
    discharge.stripe_session_id = session.id
    discharge.save(update_fields=["stripe_session_id"])
    return redirect(session.url)


@login_required
@user_passes_test(is_patient)
def payment_success_view(request):
    session_id = request.GET.get("session_id", "")
    if not session_id:
        messages.error(request, "Missing payment session information.")
        return redirect("patient-discharge-summary")

    if not settings.STRIPE_SECRET_KEY:
        messages.error(request, "Stripe is not configured. Please contact support.")
        return redirect("patient-discharge-summary")

    stripe.api_key = settings.STRIPE_SECRET_KEY
    session = stripe.checkout.Session.retrieve(session_id)

    payment = Payment.objects.filter(
        stripe_session_id=session_id, user=request.user
    ).first()
    if not payment:
        messages.error(request, "Payment record not found.")
        return redirect("patient-discharge-summary")

    if session.payment_status == "paid":
        payment.status = "paid"
        payment.stripe_payment_intent = session.payment_intent or ""
        payment.save(update_fields=["status", "stripe_payment_intent"])
        if payment.discharge and not payment.discharge.is_paid:
            payment.discharge.is_paid = True
            payment.discharge.paid_at = timezone.now()
            payment.discharge.stripe_session_id = session_id
            payment.discharge.save(update_fields=["is_paid", "paid_at", "stripe_session_id"])

        if request.user.email:
            send_mail(
                subject="Payment receipt - Hospital Management",
                message=(
                    "Thank you for your payment.\n\n"
                    f"Amount: {payment.amount} {payment.currency.upper()}\n"
                    f"Status: {payment.get_status_display()}\n"
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[request.user.email],
                fail_silently=True,
            )

        messages.success(request, "Payment successful. Receipt sent to your email.")
    else:
        payment.status = "failed"
        payment.save(update_fields=["status"])
        messages.error(request, "Payment not completed. Please try again.")

    return render(request, "payments/success.html", {"payment": payment})


@login_required
@user_passes_test(is_patient)
def payment_cancel_view(request):
    session_id = request.GET.get("session_id", "")
    if session_id:
        payment = Payment.objects.filter(
            stripe_session_id=session_id, user=request.user
        ).first()
        if payment and payment.status != "paid":
            payment.status = "failed"
            payment.save(update_fields=["status"])
    messages.error(request, "Payment cancelled. You can try again anytime.")
    return render(request, "payments/cancel.html")


@login_required
@user_passes_test(is_patient)
def payment_history_view(request):
    payments = Payment.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "payments/history.html", {"payments": payments})


@login_required
@user_passes_test(is_patient)
def patient_payments_view(request):
    discharge = (
        DischargeDetails.objects.filter(patient__user=request.user)
        .order_by("-discharge_date")
        .first()
    )
    payment = None
    if discharge:
        payment = Payment.objects.filter(discharge=discharge).order_by("-created_at").first()
        if payment and payment.status == "paid":
            discharge.is_paid = True
    return render(
        request,
        "hospital/patient_payments.html",
        {"discharge": discharge, "payment": payment},
    )


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE", "")
    if not settings.STRIPE_WEBHOOK_SECRET:
        return HttpResponse(status=400)
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except Exception:
        return HttpResponse(status=400)

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        discharge_id = session.get("metadata", {}).get("discharge_id")
        if discharge_id:
            discharge = DischargeDetails.objects.filter(id=discharge_id).first()
            if discharge and not discharge.is_paid:
                discharge.is_paid = True
                discharge.paid_at = timezone.now()
                discharge.stripe_session_id = session.get("id", "")
                discharge.save(update_fields=["is_paid", "paid_at", "stripe_session_id"])
        payment = Payment.objects.filter(stripe_session_id=session.get("id", "")).first()
        if payment and payment.status != "paid":
            payment.status = "paid"
            payment.stripe_payment_intent = session.get("payment_intent") or ""
            payment.save(update_fields=["status", "stripe_payment_intent"])

    return HttpResponse(status=200)
