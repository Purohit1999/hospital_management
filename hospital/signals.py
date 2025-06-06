from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Prescription, Invoice
from django.utils import timezone

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
