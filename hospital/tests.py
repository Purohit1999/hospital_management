from django.contrib.auth.models import Group, User
from django.test import TestCase, override_settings
from django.urls import reverse

from .models import Appointment, Doctor, Patient


@override_settings(
    STORAGES={
        "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
        "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
    }
)
class AdminPatientViewsTests(TestCase):
    def setUp(self):
        self.admin_user = User.objects.create_user(
            username="admin_user",
            password="admin_pass",
            is_staff=True,
            is_superuser=True,
        )

        self.doctor_user = User.objects.create_user(
            username="doctor_user",
            password="doctor_pass",
        )
        self.patient_user = User.objects.create_user(
            username="patient_user",
            password="patient_pass",
            email="patient@example.com",
        )

        self.doctor = Doctor.objects.create(user=self.doctor_user, status=True)
        self.patient = Patient.objects.create(user=self.patient_user)

        Group.objects.get_or_create(name="PATIENT")
        Group.objects.get_or_create(name="DOCTOR")

    def test_patient_edit_updates_record(self):
        self.client.force_login(self.admin_user)
        url = reverse("edit-patient", args=[self.patient.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        post_data = {
            "first_name": "Pat",
            "last_name": "Patient",
            "username": self.patient_user.username,
            "email": "updated@example.com",
            "address": "221B Baker Street",
            "mobile": "123456789",
            "symptoms": "Headache",
            "assignedDoctorId": "",
        }
        response = self.client.post(url, data=post_data, follow=True)
        self.assertEqual(response.status_code, 200)

        self.patient.refresh_from_db()
        self.patient_user.refresh_from_db()
        self.assertEqual(self.patient.mobile, "123456789")
        self.assertEqual(self.patient_user.email, "updated@example.com")

    def test_patient_delete_blocked_when_appointments_exist(self):
        Appointment.objects.create(
            patient=self.patient,
            doctor=self.doctor,
            status="pending",
        )

        self.client.force_login(self.admin_user)
        url = reverse("delete-patient", args=[self.patient.pk])
        response = self.client.get(url, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(Patient.objects.filter(pk=self.patient.pk).exists())
