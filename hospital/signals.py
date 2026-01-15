import logging

from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.contrib.auth.models import Group, User
from django.utils import timezone

from .models import Prescription, Invoice, Patient, Doctor

logger = logging.getLogger(__name__)

@receiver(post_save, sender=Prescription)
def create_invoice_from_prescription(sender, instance, created, **kwargs):
    if created:
        patient = instance.appointment.patient
        amount = 1000  # You can make this dynamic
        Invoice.objects.create(
            patient=patient,
            amount=amount,
            issued_date=timezone.now(),
            created_by=instance.created_by if hasattr(instance, 'created_by') else None
        )


def _ensure_patient_for_user(user):
    if not user or user.is_staff or user.is_superuser:
        logger.info(
            "Skipping Patient auto-create for staff/superuser or missing user",
            extra={"user_id": getattr(user, "id", None)},
        )
        return

    patient_group = Group.objects.filter(name="PATIENT").first()
    if not patient_group or not user.groups.filter(id=patient_group.id).exists():
        logger.info(
            "User not in PATIENT group; skipping Patient auto-create",
            extra={"user_id": user.id, "username": user.username},
        )
        return

    try:
        patient, created = Patient.objects.get_or_create(
            user=user, defaults={"status": False}
        )
        if created:
            logger.info(
                "Created Patient profile",
                extra={"user_id": user.id, "patient_id": patient.id},
            )
        else:
            logger.info(
                "Patient profile already exists",
                extra={"user_id": user.id, "patient_id": patient.id},
            )
        logger.info(
            "Patient profile ensured (created=%s)",
            created,
            extra={"user_id": user.id},
        )
    except Exception:
        logger.exception(
            "Failed to auto-create Patient profile",
            extra={"user_id": user.id, "username": user.username},
        )


def _ensure_doctor_for_user(user):
    if not user or user.is_staff or user.is_superuser:
        logger.info(
            "Skipping Doctor auto-create for staff/superuser or missing user",
            extra={"user_id": getattr(user, "id", None)},
        )
        return

    doctor_group = Group.objects.filter(name="DOCTOR").first()
    if not doctor_group or not user.groups.filter(id=doctor_group.id).exists():
        logger.info(
            "User not in DOCTOR group; skipping Doctor auto-create",
            extra={"user_id": user.id, "username": user.username},
        )
        return

    try:
        doctor, created = Doctor.objects.get_or_create(
            user=user, defaults={"status": False}
        )
        if created:
            logger.info(
                "Created Doctor profile",
                extra={"user_id": user.id, "doctor_id": doctor.id},
            )
        else:
            logger.info(
                "Doctor profile already exists",
                extra={"user_id": user.id, "doctor_id": doctor.id},
            )
        logger.info(
            "Doctor profile ensured (created=%s)",
            created,
            extra={"user_id": user.id},
        )
    except Exception:
        logger.exception(
            "Failed to auto-create Doctor profile",
            extra={"user_id": user.id, "username": user.username},
        )


@receiver(post_save, sender=User)
def ensure_patient_on_user_create(sender, instance, created, **kwargs):
    if not created:
        return
    logger.info(
        "User saved; checking PATIENT group for Patient auto-create",
        extra={"user_id": instance.id},
    )
    _ensure_patient_for_user(instance)


@receiver(m2m_changed, sender=User.groups.through)
def ensure_patient_on_group_add(sender, instance, action, pk_set, **kwargs):
    if action != "post_add" or not pk_set:
        return
    logger.info(
        "User groups post_add fired; pk_set=%s",
        pk_set,
        extra={"user_id": instance.id},
    )
    patient_group = Group.objects.filter(name="PATIENT").first()
    doctor_group = Group.objects.filter(name="DOCTOR").first()

    if patient_group and patient_group.id in pk_set:
        logger.info(
            "PATIENT group added to user; ensuring Patient profile",
            extra={"user_id": instance.id},
        )
        _ensure_patient_for_user(instance)
    else:
        logger.info(
            "Group add does not include PATIENT; skipping Patient auto-create",
            extra={"user_id": instance.id},
        )

    if doctor_group and doctor_group.id in pk_set:
        logger.info(
            "DOCTOR group added to user; ensuring Doctor profile",
            extra={"user_id": instance.id},
        )
        _ensure_doctor_for_user(instance)
    else:
        logger.info(
            "Group add does not include DOCTOR; skipping Doctor auto-create",
            extra={"user_id": instance.id},
        )
