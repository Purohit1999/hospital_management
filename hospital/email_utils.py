import logging
from datetime import timedelta

from django.conf import settings
from django.core.mail import EmailMessage, send_mail
from django.db import IntegrityError
from django.utils import timezone

from .models import EmailLog

logger = logging.getLogger(__name__)


def _log_email(to_email, subject, event_type, status, error_message="", dedupe_key=""):
    try:
        EmailLog.objects.create(
            to_email=to_email,
            subject=subject,
            event_type=event_type,
            status=status,
            error_message=error_message or "",
            dedupe_key=dedupe_key or "",
        )
    except Exception:
        logger.exception(
            "Failed to record EmailLog",
            extra={"to": to_email, "event_type": event_type},
        )

def _invoice_dedupe_key(invoice):
    if invoice and invoice.patient_id:
        return f"invoice:{invoice.patient_id}"
    return ""


def send_consultation_email(appointment, event_type):
    subject = "Hospital Appointment Notification"
    body = (
        f"Appointment details:\n"
        f"Doctor: {appointment.doctor.user.get_full_name()}\n"
        f"Patient: {appointment.patient.user.get_full_name()}\n"
        f"Date/Time: {appointment.date_time}\n"
        f"Status: {appointment.status}\n"
    )

    recipients = []
    if appointment.doctor and appointment.doctor.user and appointment.doctor.user.email:
        recipients.append(appointment.doctor.user.email)
    if appointment.patient and appointment.patient.user and appointment.patient.user.email:
        recipients.append(appointment.patient.user.email)

    if not recipients:
        _log_email("", subject, event_type, "FAILED", "No recipient emails found.")
        return False

    try:
        send_mail(
            subject=subject,
            message=body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=recipients,
            fail_silently=False,
        )
        for email in recipients:
            _log_email(email, subject, event_type, "SUCCESS")
        return True
    except Exception as exc:
        logger.exception(
            "Failed to send appointment email",
            extra={"event_type": event_type},
        )
        for email in recipients:
            _log_email(email, subject, event_type, "FAILED", str(exc))
        return False


def send_invoice_email(invoice, pdf_bytes):
    subject = "Your Hospital Invoice"
    to_email = invoice.patient.user.email if invoice.patient and invoice.patient.user else ""
    dedupe_key = _invoice_dedupe_key(invoice)

    if not to_email:
        _log_email(
            to_email,
            subject,
            "invoice_email",
            "FAILED",
            "missing_recipient_email",
            dedupe_key=dedupe_key,
        )
        return False

    if not getattr(settings, "EMAIL_ENABLED", False):
        logger.warning(
            "Email disabled: missing credentials. Invoice email skipped.",
            extra={"invoice": invoice.id},
        )
        _log_email(
            to_email,
            subject,
            "invoice_email",
            "SKIPPED",
            "email_disabled",
            dedupe_key=dedupe_key,
        )
        return False

    pending_log = None
    try:
        cooldown_minutes = int(
            getattr(settings, "INVOICE_EMAIL_COOLDOWN_MINUTES", 5)
        )
        cooldown_window = timezone.now() - timedelta(minutes=cooldown_minutes)
        recent = (
            EmailLog.objects.filter(
                dedupe_key=dedupe_key,
                status__in=["SUCCESS", "PENDING"],
                created_at__gte=cooldown_window,
            )
            .order_by("-created_at")
            .first()
        )
        if recent:
            _log_email(
                to_email,
                subject,
                "invoice_email",
                "SKIPPED",
                "cooldown_active",
                dedupe_key=dedupe_key,
            )
            return False

        try:
            pending_log = EmailLog.objects.create(
                to_email=to_email,
                subject=subject,
                event_type="invoice_email",
                status="PENDING",
                error_message="",
                dedupe_key=dedupe_key,
            )
        except IntegrityError:
            _log_email(
                to_email,
                subject,
                "invoice_email",
                "SKIPPED",
                "duplicate_pending",
                dedupe_key=dedupe_key,
            )
            return False

        email = EmailMessage(
            subject=subject,
            body="Please find your invoice attached.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[to_email],
            cc=[settings.ADMIN_INVOICE_EMAIL],
        )
        if pdf_bytes:
            email.attach(
                filename=f"invoice_{invoice.id}.pdf",
                content=pdf_bytes,
                mimetype="application/pdf",
            )
        email.send(fail_silently=False)
        if pending_log:
            pending_log.status = "SUCCESS"
            pending_log.error_message = ""
            pending_log.save(update_fields=["status", "error_message"])
        return True
    except Exception as exc:
        logger.exception("Failed to send invoice email", extra={"invoice": invoice.id})
        error_message = str(exc)
        if error_message and len(error_message) > 500:
            error_message = error_message[:500]
        if pending_log:
            pending_log.status = "FAILED"
            pending_log.error_message = error_message or "send_failed"
            pending_log.save(update_fields=["status", "error_message"])
        else:
            _log_email(
                to_email,
                subject,
                "invoice_email",
                "FAILED",
                error_message,
                dedupe_key=dedupe_key,
            )
        return False
