# ==============================
# Django Core Imports
# ==============================
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseForbidden, Http404
from django.utils import timezone
from django.conf import settings
from django.utils.http import url_has_allowed_host_and_scheme
from django.db import IntegrityError
from django.db.models import Q
from django.db.models.deletion import ProtectedError
from django.contrib import messages
import logging
from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string

# ==============================
# Authentication & Authorization
# ==============================
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LogoutView
from django.contrib.auth.forms import AuthenticationForm

# ==============================
# CSRF & View Decorators
# ==============================
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from datetime import datetime
from io import BytesIO

# ==============================
# App-Specific Imports
# ==============================
from .models import Doctor, Patient, Appointment, DischargeDetails, Invoice, EmailLog
from .models import ConsultationRequest
from payments.models import Payment
from .forms import (
    AppointmentForm,
    PatientUserForm, PatientForm,
    DoctorUserForm, DoctorForm,
    UserForm,
    ConsultationRequestForm,
    ContactForm,          # 👈 contact form import
)

logger = logging.getLogger(__name__)


# ==============================
# Helper functions for roles
# ==============================
def is_admin(user):
    return user.is_superuser or user.is_staff


def is_doctor(user):
    return user.groups.filter(name="DOCTOR").exists()


def is_patient(user):
    return user.groups.filter(name="PATIENT").exists()


def get_current_patient(request):
    patient = Patient.objects.select_related("user").filter(user=request.user).first()
    if not patient:
        messages.error(
            request,
            "Patient profile not found. Please complete registration.",
        )
        return None
    return patient


def _get_doctor_profile_or_redirect(request, redirect_name="doctorlogin"):
    doctor = Doctor.objects.filter(user=request.user).first()
    if not doctor:
        messages.error(
            request,
            "Doctor profile missing or not approved. Please contact admin.",
        )
        logger.warning(
            "Doctor profile missing for user_id=%s",
            getattr(request.user, "id", None),
        )
        return redirect(redirect_name)
    if hasattr(doctor, "status") and not doctor.status:
        messages.error(
            request,
            "Doctor profile missing or not approved. Please contact admin.",
        )
        logger.warning(
            "Doctor profile not approved for user_id=%s doctor_id=%s",
            getattr(request.user, "id", None),
            doctor.id,
        )
        return redirect(redirect_name)
    return doctor


# ---------------- CUSTOM LOGOUT ----------------
@method_decorator(csrf_exempt, name="dispatch")
class CustomLogoutView(LogoutView):
    def post(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


# ---------------- HOME & STATIC ----------------
def home_view(request):
    return render(request, "hospital/index.html")


def aboutus_view(request):
    return render(request, "hospital/aboutus.html")


def contactus_view(request):
    """
    Contact/feedback view:
    - GET: show empty ContactForm
    - POST: validate and redirect to success page
    """
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            # Optional user feedback
            messages.success(request, "Thank you for your feedback!")
            return redirect("contact-success")
    else:
        form = ContactForm()

    return render(request, "hospital/contactus.html", {"form": form})


def contact_success_view(request):
    """ Simple success page after contact form submission. """
    return render(request, "hospital/contactussuccess.html")


# ---------------- DEMO LOGINS ----------------
def demo_logins_view(request):
    demo_users = (
        User.objects.filter(username__startswith="demo_p", groups__name="PATIENT")
        .distinct()
        .order_by("username")
    )
    return render(
        request,
        "hospital/demo_logins.html",
        {"demo_users": demo_users},
    )


# ---------------- PUBLIC CONSULTATION ----------------
def book_consultation_view(request):
    if request.method == "POST":
        form = ConsultationRequestForm(request.POST)
        if form.is_valid():
            consultation = form.save()
            if consultation.email:
                send_mail(
                    subject="Consultation request received",
                    message=(
                        "Thanks — we’ve received your consultation request.\n"
                        "Our team will contact you soon.\n\n"
                        f"Requested: {consultation.preferred_date} "
                        f"{consultation.preferred_time}\n"
                    ),
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[consultation.email],
                    fail_silently=True,
                )
            send_mail(
                subject="New consultation request",
                message=(
                    "A new consultation request has been submitted.\n\n"
                    f"Name: {consultation.full_name}\n"
                    f"Email: {consultation.email}\n"
                    f"Phone: {consultation.phone}\n"
                    f"Preferred: {consultation.preferred_date} "
                    f"{consultation.preferred_time}\n"
                    f"Message: {consultation.message}\n"
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.ADMIN_EMAIL],
                fail_silently=True,
            )
            messages.success(
                request,
                "Thanks — we’ll contact you soon.",
            )
            return redirect("book-consultation")
    else:
        form = ConsultationRequestForm()

    return render(
        request,
        "hospital/book_consultation.html",
        {"form": form},
    )


# ---------------- ROLE SELECTION ----------------
def adminclick_view(request):
    return render(request, "hospital/adminclick.html")


def doctorclick_view(request):
    return render(request, "hospital/doctorclick.html")


def patientclick_view(request):
    return render(request, "hospital/patientclick.html")


# ---------------- SIGNUP ----------------
def admin_signup_view(request):
    return render(request, "hospital/adminsignup.html")


def doctor_signup_view(request):
    if request.method == "POST":
        user_form = DoctorUserForm(request.POST)
        doctor_form = DoctorForm(request.POST, request.FILES)
        if user_form.is_valid() and doctor_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user.password)
            user.save()

            doctor_group, _ = Group.objects.get_or_create(name="DOCTOR")
            user.groups.add(doctor_group)

            doctor = doctor_form.save(commit=False)
            doctor.user = user
            doctor.status = False
            doctor.save()
            login(request, user)
            messages.success(request, "Registration successful. Welcome!")
            return redirect("afterlogin")
    else:
        user_form = DoctorUserForm()
        doctor_form = DoctorForm()

    return render(
        request,
        "hospital/doctorsignup.html",
        {"userForm": user_form, "doctorForm": doctor_form},
    )


def patient_signup_view(request):
    if request.method == "POST":
        user_form = PatientUserForm(request.POST)
        patient_form = PatientForm(request.POST, request.FILES)
        if user_form.is_valid() and patient_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user.password)
            user.save()

            group, _ = Group.objects.get_or_create(name="PATIENT")
            user.groups.add(group)

            patient = patient_form.save(commit=False)
            patient.user = user
            patient.save()
            Patient.objects.get_or_create(user=user)
            login(request, user)
            logger.info("Auto-login after signup", extra={"user_id": user.id})
            messages.success(request, "Registration successful. Welcome!")
            return redirect("patient-dashboard")
    else:
        user_form = PatientUserForm()
        patient_form = PatientForm()

    return render(
        request,
        "hospital/patientsignup.html",
        {"userForm": user_form, "patientForm": patient_form},
    )


# ---------------- LOGIN REDIRECT ----------------
def afterlogin_view(request):
    if request.user.groups.filter(name="DOCTOR").exists():
        return redirect("doctor-dashboard")
    elif request.user.groups.filter(name="PATIENT").exists():
        return redirect("patient-dashboard")
    elif request.user.is_superuser:
        return redirect("admin-dashboard")
    return redirect("home")


# ---------------- ADMIN LOGIN ----------------
def adminlogin_view(request):
    """
    Admin login view.
    Allows staff/superusers to log in and then routes via `afterlogin_view`.
    """
    if request.method == "POST":
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)

            # Only allow staff/superuser as admin
            if user is not None and user.is_staff:
                login(request, user)
                return redirect("afterlogin")
            else:
                messages.error(
                    request,
                    "Access denied: You are not an admin user.",
                )
        else:
            messages.error(request, "Invalid credentials. Please try again.")
    else:
        form = AuthenticationForm()

    return render(request, "hospital/adminlogin.html", {"form": form})


# ---------------- DOCTOR LOGIN ----------------
def doctor_login_view(request):
    next_url = request.GET.get("next") or request.POST.get("next") or ""
    error_message = None

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user and is_doctor(user) and Doctor.objects.filter(user=user).exists():
                login(request, user)
                redirect_to = request.POST.get("next") or request.GET.get("next")
                if redirect_to and url_has_allowed_host_and_scheme(
                    redirect_to, allowed_hosts={request.get_host()}
                ):
                    return redirect(redirect_to)
                return redirect("doctor-dashboard")
            error_message = (
                "Access denied: Your doctor profile is missing or not approved."
            )
        else:
            error_message = "Invalid credentials. Please try again."
    else:
        form = AuthenticationForm()

    return render(
        request,
        "hospital/doctorlogin.html",
        {"form": form, "error": error_message, "next": next_url},
    )


def patient_login_view(request):
    """
    Handle patient login, redirecting to the requested page (next) or dashboard.
    """
    next_url = request.GET.get("next") or request.POST.get("next") or ""
    error_message = None
    username_value = request.POST.get("username", "") if request.method == "POST" else ""

    if request.method == "POST":
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user and (is_patient(user) or Patient.objects.filter(user=user).exists()):
                login(request, user)
                redirect_to = request.POST.get("next") or request.GET.get("next")
                if redirect_to and url_has_allowed_host_and_scheme(
                    redirect_to, allowed_hosts={request.get_host()}
                ):
                    return redirect(redirect_to)
                return redirect("patient-dashboard")
            error_message = "Access denied: Please log in using a patient account."
        else:
            error_message = "Invalid username or password."
            if "@" in request.POST.get("username", ""):
                email_input = request.POST.get("username", "").strip()
                password_input = request.POST.get("password", "")
                user_by_email = (
                    User.objects.filter(email__iexact=email_input)
                    .order_by("id")
                    .first()
                )
                if user_by_email:
                    user = authenticate(
                        request,
                        username=user_by_email.username,
                        password=password_input,
                    )
                    if user and (is_patient(user) or Patient.objects.filter(user=user).exists()):
                        login(request, user)
                        redirect_to = request.POST.get("next") or request.GET.get("next")
                        if redirect_to and url_has_allowed_host_and_scheme(
                            redirect_to, allowed_hosts={request.get_host()}
                        ):
                            return redirect(redirect_to)
                        return redirect("patient-dashboard")

    context = {
        "error": error_message,
        "next": next_url,
        "username": username_value,
    }
    return render(request, "hospital/patient_login.html", context)


# ---------------- DOCTOR DASHBOARD ----------------
@login_required(login_url="doctorlogin")
@user_passes_test(is_doctor)
def doctor_dashboard_view(request):
    """
    Doctor dashboard:
    - Loads doctor profile linked to the logged-in user
    - If no doctor profile exists, show a friendly message instead of 404
    """
    doctor = _get_doctor_profile_or_redirect(request, redirect_name="doctorclick")
    if not isinstance(doctor, Doctor):
        return doctor

    return render(request, "hospital/doctor_dashboard.html", {"doctor": doctor})


@login_required(login_url="doctorlogin")
@user_passes_test(is_doctor)
def doctor_view_patient_view(request):
    doctor = _get_doctor_profile_or_redirect(request, redirect_name="doctorclick")
    if not isinstance(doctor, Doctor):
        return doctor

    patients = Patient.objects.filter(appointment__doctor=doctor).distinct()
    return render(request, "hospital/doctor_view_patient.html", {"patients": patients})


@login_required(login_url="doctorlogin")
@user_passes_test(is_doctor)
def doctor_view_appointment_view(request):
    doctor = _get_doctor_profile_or_redirect(request, redirect_name="doctorclick")
    if not isinstance(doctor, Doctor):
        return doctor

    logger.info(
        "Doctor appointment view user_id=%s doctor_id=%s",
        getattr(request.user, "id", None),
        doctor.id,
    )
    appointments = Appointment.objects.filter(doctor=doctor).select_related(
        "patient__user"
    )
    return render(
        request,
        "hospital/doctor_view_appointment.html",
        {"appointments": appointments},
    )


@login_required(login_url="doctorlogin")
@user_passes_test(is_doctor)
def doctor_view_discharge_patient_view(request):
    """
    Doctor view of discharged patients.
    Uses DischargeDetails.doctor foreign key.
    """
    doctor = _get_doctor_profile_or_redirect(request, redirect_name="doctor-dashboard")
    if not isinstance(doctor, Doctor):
        return doctor

    discharged_patients = DischargeDetails.objects.filter(
        doctor=doctor
    ).order_by("-discharge_date")

    return render(
        request,
        "hospital/doctor_view_discharge_patient.html",
        {"discharged_patients": discharged_patients},
    )


# ---------------- DOCTOR APPROVAL (ADMIN) ----------------
@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def admin_approve_doctor_view(request):
    try:
        doctors = Doctor.objects.filter(status=False).select_related("user")
        context = {"pending_doctors": doctors}
    except Exception:
        logger.exception(
            "Failed to load pending doctors",
            extra={"path": request.path, "user": request.user.username},
        )
        context = {
            "pending_doctors": [],
            "error": "Unable to load pending doctors right now. Please try again.",
        }
    return render(request, "hospital/admin_approve_doctor.html", context)


# ---------------- PATIENT DASHBOARD ----------------
@login_required(login_url="patientlogin")
@user_passes_test(is_patient)
def patient_dashboard_view(request):
    """
    Patient dashboard:
    - Shows patient info
    - Shows latest appointment's doctor & date (if any)
    - Displays any success messages (e.g., after booking)
    """
    patient = get_current_patient(request)
    if not patient:
        return redirect("patientsignup")

    latest_appointment = (
        Appointment.objects.filter(patient=patient)
        .select_related("doctor__user")
        .order_by("-date_time")
        .first()
    )
    doctor = latest_appointment.doctor if latest_appointment else None

    invoices = Invoice.objects.filter(patient=patient).order_by("-id")
    discharges = DischargeDetails.objects.filter(patient=patient).order_by(
        "-discharge_date"
    )
    payments_count = Payment.objects.filter(patient=patient, status="paid").count()
    email_logs = []
    if patient.user and patient.user.email:
        email_logs = EmailLog.objects.filter(
            to_email=patient.user.email
        ).order_by("-id")

    context = {
        "patient": patient,
        "doctor": doctor,
        "latest_appointment": latest_appointment,
        "invoices": invoices,
        "discharges": discharges,
        "email_logs": email_logs,
        "appointments_count": Appointment.objects.filter(patient=patient).count(),
        "invoices_count": invoices.count(),
        "payments_count": payments_count,
    }
    return render(request, "hospital/patient_dashboard.html", context)


# ---------------- ADMIN DASHBOARD ----------------
@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def admin_dashboard_view(request):
    context = {
        # how many doctors are still waiting for approval
        "pending_doctors": Doctor.objects.filter(status=False).count(),
        # total patients (you could also track pending separately if needed)
        "pending_patients": Patient.objects.count(),
        # appointments that are still pending
        "pending_appointments": Appointment.objects.filter(
            status="pending"
        ).count(),
        # recent / approved doctors and recent patients for the tables
        "recent_doctors": Doctor.objects.select_related("user")
        .filter(status=True)
        .order_by("-id")[:5],
        "recent_patients": Patient.objects.select_related("user").order_by("-id")[:5],
    }
    return render(request, "hospital/admin_dashboard.html", context)


# ---------------- DOCTOR ADMIN ----------------
@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def admin_doctor_view(request):
    return render(request, "hospital/admin_doctor.html")


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def admin_view_doctor_view(request):
    doctors = Doctor.objects.select_related("user").all()
    return render(request, "hospital/admin_view_doctor.html", {"doctors": doctors})


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def admin_consultation_requests_view(request):
    requests = ConsultationRequest.objects.order_by("-created_at")
    return render(
        request,
        "hospital/admin_consultation_requests.html",
        {"requests": requests},
    )


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def admin_add_doctor_view(request):
    if request.method == "POST":
        user_form = DoctorUserForm(request.POST)
        doctor_form = DoctorForm(request.POST, request.FILES)
        if user_form.is_valid() and doctor_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user.password)
            user.save()

            group, _ = Group.objects.get_or_create(name="DOCTOR")
            user.groups.add(group)

            doctor = doctor_form.save(commit=False)
            doctor.user = user
            doctor.save()
            return redirect("admin-view-doctor")
    else:
        user_form = DoctorUserForm()
        doctor_form = DoctorForm()

    return render(
        request,
        "hospital/admin_add_doctor.html",
        {"userForm": user_form, "doctorForm": doctor_form},
    )


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def edit_doctor_view(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    user = doctor.user
    if request.method == "POST":
        user_form = UserForm(request.POST, instance=user)
        doctor_form = DoctorForm(request.POST, request.FILES, instance=doctor)
        if user_form.is_valid() and doctor_form.is_valid():
            user_form.save()
            doctor_form.save()
            messages.success(request, "Doctor updated successfully.")
            return redirect("admin-view-doctor")
    else:
        user_form = UserForm(instance=user)
        doctor_form = DoctorForm(instance=doctor)

    return render(
        request,
        "hospital/edit_doctor.html",
        {"userForm": user_form, "doctorForm": doctor_form},
    )


# ---------------- PATIENT ADMIN ----------------
@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def admin_patient_view(request):
    return render(request, "hospital/admin_patient.html")


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def admin_view_patient_view(request):
    patients = Patient.objects.select_related("user").order_by("-id")
    logger.info(
        "admin_view_patient_view count=%s",
        patients.count(),
        extra={"path": request.path, "user": request.user.username},
    )
    return render(
        request, "hospital/admin_view_patient.html", {"patients": patients}
    )


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def admin_add_patient_view(request):
    if request.method == "POST":
        user_form = PatientUserForm(request.POST)
        patient_form = PatientForm(request.POST, request.FILES)
        if user_form.is_valid() and patient_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user.password)
            user.save()

            group, _ = Group.objects.get_or_create(name="PATIENT")
            user.groups.add(group)

            patient = patient_form.save(commit=False)
            patient.user = user
            patient.save()
            return redirect("admin-view-patient")
    else:
        user_form = PatientUserForm()
        patient_form = PatientForm()

    return render(
        request,
        "hospital/admin_add_patient.html",
        {"userForm": user_form, "patientForm": patient_form},
    )


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def edit_patient_view(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    user = patient.user
    if request.method == "POST":
        user_form = UserForm(request.POST, instance=user)
        patient_form = PatientForm(request.POST, request.FILES, instance=patient)
        if user_form.is_valid() and patient_form.is_valid():
            user_form.save()
            patient_form.save()
            messages.success(request, "Patient updated successfully.")
            return redirect("admin-view-patient")
    else:
        user_form = UserForm(instance=user)
        patient_form = PatientForm(instance=patient)

    return render(
        request,
        "hospital/edit_patient.html",
        {"userForm": user_form, "patientForm": patient_form},
    )


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def delete_patient_view(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    user = patient.user
    if Appointment.objects.filter(patient=patient).exists():
        messages.error(
            request,
            "Cannot delete patient because related appointments exist. "
            "Please remove appointments first.",
        )
        return redirect("admin-view-patient")
    try:
        patient.delete()
    except (ProtectedError, IntegrityError):
        messages.error(
            request,
            "Cannot delete patient because related appointments exist. "
            "Please remove appointments first.",
        )
        return redirect("admin-view-patient")
    if user:
        user.delete()
    messages.success(request, "Patient deleted successfully.")
    return redirect("admin-view-patient")


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def approve_patient_view(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    patient.status = True
    patient.save()
    return redirect("admin-approve-patient")


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def reject_patient_view(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    user = patient.user
    patient.delete()
    user.delete()
    return redirect("admin-approve-patient")


# ---------------- DISCHARGE PATIENT (PATIENT VIEW) ----------------
@login_required(login_url="patientlogin")
@user_passes_test(is_patient)
def patient_discharge_summary_view(request):
    patient = get_current_patient(request)
    if not patient:
        return redirect("patientsignup")
    discharges = DischargeDetails.objects.filter(
        patient=patient
    ).order_by("-discharge_date")
    payments = Payment.objects.filter(patient=patient).select_related("discharge")
    payments_by_discharge = {
        payment.discharge_id: payment for payment in payments if payment.discharge_id
    }

    for discharge in discharges:
        discharge.days_spent = (
            discharge.discharge_date - discharge.admission_date
        ).days or 1
        discharge.payment = payments_by_discharge.get(discharge.id)
        if discharge.payment and discharge.payment.status == "paid":
            discharge.is_paid = True

    context = {
        "discharges": discharges,
        "patient": patient,
        "payments_by_discharge": payments_by_discharge,
    }
    return render(request, "hospital/patient_discharge.html", context)


# ---------------- DISCHARGE PATIENT (ADMIN LISTS) ----------------
@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def admin_approve_patient_view(request):
    patients = (
        Patient.objects.filter(status=False)
        .filter(dischargedetails__isnull=True)
        .select_related("user")
        .order_by("-id")
    )
    logger.info(
        "admin_approve_patient_view pending_count=%s",
        patients.count(),
        extra={"path": request.path, "user": request.user.username},
    )
    return render(
        request,
        "hospital/admin_approve_patient.html",
        {"patients": patients},
    )


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def admin_discharge_patient_view(request):
    patients = (
        Patient.objects.filter(status=True)
        .filter(dischargedetails__isnull=True)
        .select_related("user")
        .order_by("-id")
    )
    logger.info(
        "admin_discharge_patient_view eligible_count=%s",
        patients.count(),
        extra={"path": request.path, "user": request.user.username},
    )
    return render(
        request,
        "hospital/admin_discharge_patient.html",
        {"patients": patients},
    )


# ---------------- APPOINTMENTS ----------------
@login_required(login_url="patientlogin")
@user_passes_test(is_patient)
def patient_book_appointment_view(request):
    """
    Patient-facing appointment booking.
    After successful booking, redirect to dashboard with a success message.
    """
    patient = get_current_patient(request)
    if not patient:
        return redirect("patientsignup")

    if request.method == "POST":
        form = AppointmentForm(request.POST)
        if "patient" in form.fields:
            form.fields["patient"].required = False
        if "status" in form.fields:
            form.fields["status"].required = False
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = patient
            appointment.created_by = request.user
            appointment.updated_by = request.user
            if hasattr(appointment, "status") and not appointment.status:
                appointment.status = "pending"
            appointment.save()

            messages.success(request, "Your appointment has been booked successfully.")
            return redirect("patient-appointment-list")
        messages.error(request, "Please correct the errors and try again.")
    else:
        form = AppointmentForm()
        if "patient" in form.fields:
            form.fields["patient"].required = False
        if "status" in form.fields:
            form.fields["status"].required = False

    return render(
        request,
        "hospital/patient_book_appointment.html",
        {"form": form},
    )


@login_required(login_url="patientlogin")
@user_passes_test(is_patient)
def patient_appointment_list_view(request):
    patient = get_current_patient(request)
    if not patient:
        return redirect("patientsignup")
    appointments = Appointment.objects.filter(patient=patient).order_by("-date_time")
    return render(
        request,
        "appointments/list.html",
        {"appointments": appointments},
    )


# ---------------- ADMIN / OTHER VIEWS ----------------
@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def list_appointments(request):
    appointments = (
        Appointment.objects.select_related("patient", "doctor")
        .filter(date_time__gte=timezone.now())
    )
    return render(
        request,
        "appointments/list.html",
        {"appointments": appointments},
    )


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def appointment_detail(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    return render(
        request,
        "appointments/detail.html",
        {"appointment": appointment},
    )


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def admin_view_appointment(request):
    appointments = Appointment.objects.select_related(
        "doctor__user", "patient__user"
    ).all()
    return render(
        request,
        "hospital/admin_view_appointment.html",
        {"appointments": appointments},
    )


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def admin_appointment_view(request):
    return render(request, "hospital/admin_appointment.html")


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def admin_approve_appointment_view(request):
    appointments = Appointment.objects.select_related(
        "doctor__user", "patient__user"
    ).filter(status="pending")
    return render(
        request,
        "hospital/admin_approve_appointment.html",
        {"appointments": appointments},
    )


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def approve_appointment_view(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    appointment.status = "confirmed"
    appointment.save()
    messages.success(request, "Appointment approved successfully.")
    return redirect("admin-approve-appointment")


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def reject_appointment_view(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    appointment.status = "cancelled"
    appointment.save()
    messages.success(request, "Appointment rejected successfully.")
    return redirect("admin-approve-appointment")


# ---------------- SPECIALISATION VIEW ----------------
@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def admin_view_doctor_specialisation(request):
    try:
        doctors = Doctor.objects.select_related("user").filter(status=True)
        context = {"doctors": doctors}
    except Exception:
        logger.exception(
            "Failed to load doctor specialisations",
            extra={"path": request.path, "user": request.user.username},
        )
        context = {
            "doctors": [],
            "error": "Unable to load doctor specialisations right now.",
        }
    return render(request, "hospital/admin_view_doctor_specialisation.html", context)


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def admin_add_appointment_view(request):
    if request.method == "POST":
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.created_by = request.user
            appointment.updated_by = request.user
            appointment.save()
            messages.success(request, "Appointment added successfully.")
            return redirect("admin-view-appointment")
    else:
        form = AppointmentForm()

    return render(
        request,
        "hospital/admin_add_appointment.html",
        {"form": form},
    )


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def admin_update_appointment_view(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    if request.method == "POST":
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.updated_by = request.user
            appointment.save()
            messages.success(request, "Appointment updated successfully.")
            return redirect("admin-view-appointment")
    else:
        form = AppointmentForm(instance=appointment)

    return render(
        request,
        "hospital/admin_update_appointment.html",
        {"form": form, "appointment": appointment},
    )


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def admin_delete_appointment_view(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    appointment.delete()
    messages.success(request, "Appointment deleted successfully.")
    return redirect("admin-view-appointment")


# ---------------- DOCTOR APPROVAL / SEARCH ----------------
@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def approve_doctor_view(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    doctor.status = True
    doctor.save()
    messages.success(request, "Doctor approved successfully.")
    return redirect("admin-approve-doctor")


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def reject_doctor_view(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    user = doctor.user
    doctor.delete()
    if user:
        user.delete()
    messages.success(request, "Doctor has been rejected and removed.")
    return redirect("admin-approve-doctor")


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def update_doctor_view(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    user = doctor.user
    if request.method == "POST":
        user_form = UserForm(request.POST, instance=user)
        doctor_form = DoctorForm(request.POST, request.FILES, instance=doctor)
        if user_form.is_valid() and doctor_form.is_valid():
            user_form.save()
            doctor_form.save()
            return redirect("admin-view-doctor")
    else:
        user_form = UserForm(instance=user)
        doctor_form = DoctorForm(instance=doctor)

    return render(
        request,
        "hospital/edit_doctor.html",
        {"userForm": user_form, "doctorForm": doctor_form},
    )


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def delete_doctor_view(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    user = doctor.user
    if Appointment.objects.filter(doctor=doctor).exists():
        messages.error(
            request,
            "Cannot delete doctor because related appointments exist. "
            "Please remove appointments first.",
        )
        return redirect("admin-view-doctor")
    try:
        doctor.delete()
    except (ProtectedError, IntegrityError):
        messages.error(
            request,
            "Cannot delete doctor because related appointments exist. "
            "Please remove appointments first.",
        )
        return redirect("admin-view-doctor")
    if user:
        user.delete()
    messages.success(request, "Doctor deleted successfully.")
    return redirect("admin-view-doctor")


@login_required(login_url="doctorlogin")
@user_passes_test(is_doctor)
def doctor_search_patient_view(request):
    query = request.GET.get("query", "")
    doctor = _get_doctor_profile_or_redirect(request, redirect_name="doctor-dashboard")
    if not isinstance(doctor, Doctor):
        return doctor

    patients = (
        Patient.objects.filter(assignedDoctorId=doctor)
        .filter(
            Q(user__first_name__icontains=query)
            | Q(user__last_name__icontains=query)
            | Q(symptoms__icontains=query)
        )
        .distinct()
    )

    return render(
        request,
        "hospital/doctor_view_patient.html",
        {"patients": patients},
    )


# ---------------- BILLING / DISCHARGE ----------------
def _get_patient_admit_date(patient):
    if patient and patient.created_at:
        return patient.created_at.date()
    return timezone.now().date()


def _build_bill_context(patient, admit_date, discharge_date, total_days):
    return {
        "name": f"{patient.user.first_name} {patient.user.last_name}",
        "mobile": patient.mobile,
        "address": patient.address,
        "symptoms": patient.symptoms,
        "assignedDoctorName": patient.assignedDoctorId.user.get_full_name()
        if patient.assignedDoctorId
        else "N/A",
        "admitDate": admit_date,
        "todayDate": discharge_date,
        "day": int(total_days),
        "patientId": patient.id,
    }


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def generate_patient_bill_view(request, pk):
    patient = get_object_or_404(Patient, pk=pk)

    if DischargeDetails.objects.filter(patient=patient).exists():
        messages.warning(request, "Patient already discharged.")
        return redirect("admin-view-patient")

    admit_date = _get_patient_admit_date(patient)
    today = timezone.now().date()
    total_days = max(1, (today - admit_date).days)

    return render(
        request,
        "hospital/patient_generate_bill.html",
        _build_bill_context(patient, admit_date, today, total_days),
    )


def safe_float(value):
    """Helper: safely convert to float."""
    try:
        return float(value)
    except (ValueError, TypeError):
        return 0.0


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def discharge_patient_view(request, pk):
    patient = get_object_or_404(Patient, pk=pk)

    if DischargeDetails.objects.filter(patient=patient).exists():
        messages.warning(request, "Patient already discharged.")
        return redirect("admin-view-patient")

    admit_date = _get_patient_admit_date(patient)
    discharge_date = timezone.now().date()
    total_days = max(1, (discharge_date - admit_date).days)

    if request.method == "POST":
        room_charge = safe_float(request.POST.get("roomCharge", 0)) * total_days
        doctor_fee = safe_float(request.POST.get("doctorFee", 0))
        medicine_cost = safe_float(request.POST.get("medicineCost", 0))
        other_charge = safe_float(request.POST.get("OtherCharge", 0))
        total = room_charge + doctor_fee + medicine_cost + other_charge

        DischargeDetails.objects.create(
            patient=patient,
            doctor=patient.assignedDoctorId,
            admission_date=admit_date,
            discharge_date=discharge_date,
            summary=(
                f"Discharged due to recovery from symptoms: {patient.symptoms}"
            ),
            room_charge=room_charge,
            doctor_fee=doctor_fee,
            medicine_cost=medicine_cost,
            other_charge=other_charge,
            total=total,
        )

        context = _build_bill_context(
            patient,
            admit_date.strftime("%Y-%m-%d"),
            discharge_date.strftime("%Y-%m-%d"),
            total_days,
        )
        context.update(
            {
                "roomCharge": room_charge,
                "doctorFee": doctor_fee,
                "medicineCost": medicine_cost,
                "OtherCharge": other_charge,
                "total": total,
            }
        )
        return render(request, "hospital/patient_final_bill.html", context)

    return render(
        request,
        "hospital/patient_generate_bill.html",
        _build_bill_context(patient, admit_date, discharge_date, total_days),
    )


def _get_discharge_details(patient):
    return (
        DischargeDetails.objects.filter(patient=patient)
        .order_by("-discharge_date")
        .first()
    )


def _render_invoice_pdf(context):
    from xhtml2pdf import pisa

    html = render_to_string("hospital/download_bill.html", context)
    pdf_file = BytesIO()
    pisa_status = pisa.CreatePDF(html, dest=pdf_file)
    if pisa_status.err:
        return None
    return pdf_file.getvalue()


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def download_invoice_pdf_view(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    discharge = _get_discharge_details(patient)
    if not discharge:
        messages.error(request, "No discharge record found for this patient.")
        return redirect("admin-view-patient")

    context = {
        "patientName": patient.user.get_full_name(),
        "mobile": patient.mobile,
        "address": patient.address,
        "assignedDoctorName": discharge.doctor.user.get_full_name()
        if discharge.doctor and discharge.doctor.user
        else "N/A",
        "admitDate": discharge.admission_date,
        "releaseDate": discharge.discharge_date,
        "daySpent": max(1, (discharge.discharge_date - discharge.admission_date).days),
        "symptoms": patient.symptoms,
        "roomCharge": discharge.room_charge,
        "doctorFee": discharge.doctor_fee,
        "medicineCost": discharge.medicine_cost,
        "OtherCharge": discharge.other_charge,
        "total": discharge.total,
    }
    pdf_content = _render_invoice_pdf(context)
    if not pdf_content:
        messages.error(request, "Unable to generate PDF at this time.")
        return redirect("admin-view-patient")

    response = HttpResponse(pdf_content, content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="invoice_{patient.id}.pdf"'
    return response


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def email_invoice_view(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    discharge = _get_discharge_details(patient)
    if not discharge:
        messages.error(request, "No discharge record found for this patient.")
        return redirect("admin-view-patient")

    if not patient.user.email:
        messages.error(request, "Patient does not have an email address.")
        return redirect("admin-view-patient")

    context = {
        "patientName": patient.user.get_full_name(),
        "mobile": patient.mobile,
        "address": patient.address,
        "assignedDoctorName": discharge.doctor.user.get_full_name()
        if discharge.doctor and discharge.doctor.user
        else "N/A",
        "admitDate": discharge.admission_date,
        "releaseDate": discharge.discharge_date,
        "daySpent": max(1, (discharge.discharge_date - discharge.admission_date).days),
        "symptoms": patient.symptoms,
        "roomCharge": discharge.room_charge,
        "doctorFee": discharge.doctor_fee,
        "medicineCost": discharge.medicine_cost,
        "OtherCharge": discharge.other_charge,
        "total": discharge.total,
    }
    pdf_content = _render_invoice_pdf(context)
    if not pdf_content:
        messages.error(request, "Unable to generate PDF at this time.")
        return redirect("admin-view-patient")

    subject = "Your Hospital Invoice"
    body = (
        "Please find attached your hospital invoice.\n"
        "If you have any questions, contact us."
    )
    email = EmailMessage(
        subject=subject,
        body=body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[patient.user.email],
        cc=[settings.ADMIN_EMAIL],
    )
    email.attach(
        filename=f"invoice_{patient.id}.pdf",
        content=pdf_content,
        mimetype="application/pdf",
    )
    email.send(fail_silently=True)
    messages.success(request, "Invoice emailed successfully.")
    return redirect("admin-view-patient")
