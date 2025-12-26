from datetime import timedelta
from django.contrib.auth.models import Group, User
from django.test import TestCase, override_settings
from django.utils import timezone
from unittest.mock import patch
from django.urls import reverse

from .models import Appointment, Doctor, Patient, ConsultationRequest, DischargeDetails


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


@override_settings(
    STORAGES={
        "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
        "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
    }
)
class ConsultationRequestTests(TestCase):
    def test_get_book_consultation(self):
        response = self.client.get(reverse("book-consultation"))
        self.assertEqual(response.status_code, 200)

    def test_post_creates_consultation_request(self):
        post_data = {
            "full_name": "John Doe",
            "email": "john@example.com",
            "phone": "123456789",
            "preferred_date": "2030-01-01",
            "preferred_time": "10:30",
            "message": "Need a consultation.",
        }
        response = self.client.post(
            reverse("book-consultation"), data=post_data, follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ConsultationRequest.objects.count(), 1)

    def test_post_rejects_taken_slot(self):
        ConsultationRequest.objects.create(
            full_name="Existing",
            email="existing@example.com",
            phone="111111111",
            preferred_date="2030-01-02",
            preferred_time="09:00",
            message="Existing request",
            status="pending",
        )
        post_data = {
            "full_name": "Jane Doe",
            "email": "jane@example.com",
            "phone": "222222222",
            "preferred_date": "2030-01-02",
            "preferred_time": "09:00",
            "message": "Try same slot.",
        }
        response = self.client.post(
            reverse("book-consultation"), data=post_data, follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ConsultationRequest.objects.count(), 1)

    @patch("hospital.views.send_mail")
    def test_post_sends_emails(self, send_mail_mock):
        post_data = {
            "full_name": "Email Test",
            "email": "emailtest@example.com",
            "phone": "333333333",
            "preferred_date": "2030-01-03",
            "preferred_time": "11:15",
            "message": "Email notifications test.",
        }
        response = self.client.post(
            reverse("book-consultation"), data=post_data, follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(send_mail_mock.call_count, 2)


@override_settings(
    STORAGES={
        "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
        "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
    }
)
class DoctorLoginTests(TestCase):
    def setUp(self):
        self.doctor_user = User.objects.create_user(
            username="doctor_user",
            password="doctor_pass",
        )
        group, _ = Group.objects.get_or_create(name="DOCTOR")
        self.doctor_user.groups.add(group)
        self.doctor_profile = Doctor.objects.create(user=self.doctor_user, status=True)

    def test_doctor_login_page_renders_form(self):
        response = self.client.get(reverse("doctorlogin"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Doctor Login")
        self.assertContains(response, "<form", html=False)

    def test_doctor_dashboard_redirects_when_unauthenticated(self):
        response = self.client.get(reverse("doctor-dashboard"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/doctorlogin/?next=/doctor-dashboard/", response["Location"])

    def test_doctor_login_redirects_to_next(self):
        response = self.client.post(
            reverse("doctorlogin") + "?next=/doctor-dashboard/",
            data={
                "username": "doctor_user",
                "password": "doctor_pass",
                "next": "/doctor-dashboard/",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], "/doctor-dashboard/")

    def test_doctor_login_denies_non_doctor(self):
        non_doctor = User.objects.create_user(
            username="not_doctor",
            password="not_doctor_pass",
        )
        response = self.client.post(
            reverse("doctorlogin"),
            data={"username": "not_doctor", "password": "not_doctor_pass"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response, "Access denied: Your doctor profile is missing or not approved."
        )
        self.assertFalse(response.wsgi_request.user.is_authenticated)


@override_settings(
    STORAGES={
        "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
        "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
    }
)
class DoctorSignupTests(TestCase):
    def test_doctor_signup_page_renders(self):
        response = self.client.get(reverse("doctorsignup"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Doctor Registration")
        self.assertContains(response, "<form", html=False)

    def test_doctor_signup_creates_user_and_profile(self):
        post_data = {
            "first_name": "Doc",
            "last_name": "Tor",
            "username": "doc_user",
            "password": "doc_pass",
            "department": "Cardiology",
            "address": "1 Street",
            "mobile": "5551234",
        }
        response = self.client.post(reverse("doctorsignup"), data=post_data)
        self.assertEqual(response.status_code, 302)

        user = User.objects.get(username="doc_user")
        self.assertTrue(user.groups.filter(name="DOCTOR").exists())
        self.assertTrue(Doctor.objects.filter(user=user).exists())


@override_settings(
    STORAGES={
        "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
        "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
    }
)
class AdminModuleTests(TestCase):
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
        )
        self.doctor = Doctor.objects.create(user=self.doctor_user, status=True)
        self.patient = Patient.objects.create(
            user=self.patient_user,
            assignedDoctorId=self.doctor,
            symptoms="Cough",
        )

    def test_admin_patient_list_renders(self):
        self.client.force_login(self.admin_user)
        response = self.client.get(reverse("admin-view-patient"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Patient")

    def test_admin_add_patient_creates_record(self):
        self.client.force_login(self.admin_user)
        response = self.client.post(
            reverse("admin-add-patient"),
            data={
                "first_name": "New",
                "last_name": "Patient",
                "username": "new_patient",
                "password": "new_pass",
                "address": "1 Street",
                "mobile": "1234567890",
                "symptoms": "Fever",
                "assignedDoctorId": "",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username="new_patient").exists())
        self.assertTrue(Patient.objects.filter(user__username="new_patient").exists())

    def test_discharge_creates_discharge_details_and_pdf(self):
        self.client.force_login(self.admin_user)
        self.patient.created_at = timezone.now() - timedelta(days=2)
        self.patient.save(update_fields=["created_at"])

        discharge_response = self.client.post(
            reverse("discharge-patient", args=[self.patient.pk]),
            data={
                "roomCharge": "100",
                "doctorFee": "50",
                "medicineCost": "25",
                "OtherCharge": "10",
            },
        )
        self.assertEqual(discharge_response.status_code, 200)
        self.assertTrue(
            DischargeDetails.objects.filter(patient=self.patient).exists()
        )

        pdf_response = self.client.get(
            reverse("download-pdf", args=[self.patient.pk])
        )
        self.assertEqual(pdf_response.status_code, 200)
        self.assertEqual(pdf_response["Content-Type"], "application/pdf")
