import logging

from django.conf import settings
from django.core.mail import EmailMessage, send_mail

from .models import EmailLog

logger = logging.getLogger(__name__)


def _log_email(to_email, subject, event_type, status, error_message=""):
    try:
        EmailLog.objects.create(
            to_email=to_email,
            subject=subject,
            event_type=event_type,
            status=status,
            error_message=error_message or "",
        )
    except Exception:
        logger.exception(
            "Failed to record EmailLog",
            extra={"to": to_email, "event_type": event_type},
        )


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

    if not to_email:
        _log_email(to_email, subject, "invoice_email", "FAILED", "Missing patient email.")
        return False

    try:
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
        _log_email(to_email, subject, "invoice_email", "SUCCESS")
        return True
    except Exception as exc:
        logger.exception("Failed to send invoice email", extra={"invoice": invoice.id})
        _log_email(to_email, subject, "invoice_email", "FAILED", str(exc))
        return False
