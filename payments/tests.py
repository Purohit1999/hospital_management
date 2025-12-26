from unittest.mock import patch

from django.contrib.auth.models import Group, User
from django.core import mail
from django.test import TestCase, override_settings
from django.urls import reverse

from hospital.models import DischargeDetails, Patient
from .models import Payment


@override_settings(
    STRIPE_SECRET_KEY="sk_test_123",
    DEFAULT_FROM_EMAIL="no-reply@example.com",
    EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
    STORAGES={
        "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
        "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
    },
)
class PaymentSuccessViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="patient_user",
            password="patient_pass",
            email="patient@example.com",
        )
        group, _ = Group.objects.get_or_create(name="PATIENT")
        self.user.groups.add(group)

        self.patient = Patient.objects.create(user=self.user)
        self.discharge = DischargeDetails.objects.create(
            patient=self.patient,
            doctor=None,
            admission_date="2024-01-01",
            discharge_date="2024-01-02",
            summary="Recovered",
            room_charge=100,
            doctor_fee=100,
            medicine_cost=50,
            other_charge=20,
            total=270,
        )

        self.payment = Payment.objects.create(
            user=self.user,
            patient=self.patient,
            discharge=self.discharge,
            amount=270,
            currency="gbp",
            stripe_session_id="cs_test_123",
            status="pending",
        )

    @patch("payments.views.stripe.checkout.Session.retrieve")
    def test_payment_success_marks_paid(self, mock_retrieve):
        mock_retrieve.return_value = type(
            "Session",
            (),
            {"payment_status": "paid", "payment_intent": "pi_test_123"},
        )()

        self.client.force_login(self.user)
        url = reverse("payments-success") + "?session_id=cs_test_123"
        response = self.client.get(url)

        self.payment.refresh_from_db()
        self.assertEqual(self.payment.status, "paid")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(mail.outbox), 1)
