import logging

from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import Group, User
from django.db import IntegrityError
from django.db.models.deletion import ProtectedError
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .email_utils import send_consultation_email, send_invoice_email
from .forms_admin_dashboard import (
    AdminUserForm,
    AppointmentForm,
    DoctorForm,
    PatientForm,
)
from .models import Appointment, DischargeDetails, Doctor, Invoice, Patient
from .pdf_utils import render_invoice_pdf

logger = logging.getLogger(__name__)


def is_admin(user):
    return user.is_superuser or user.is_staff


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def adm2_doctor_list(request):
    try:
        doctors = Doctor.objects.select_related("user")
        return render(request, "hospital/admin_view_doctor.html", {"doctors": doctors})
    except Exception:
        logger.exception("adm2_doctor_list failed")
        messages.error(request, "Unable to load doctors at this time.")
        return render(request, "hospital/admin_view_doctor.html", {"doctors": []})


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def adm2_doctor_add(request):
    if request.method == "POST":
        user_form = AdminUserForm(request.POST)
        doctor_form = DoctorForm(request.POST, request.FILES)
        if user_form.is_valid() and doctor_form.is_valid():
            try:
                if not user_form.cleaned_data.get("password"):
                    messages.error(request, "Password is required.")
                    return redirect("adm2_doctor_add")
                user = user_form.save(commit=False)
                user.set_password(user.password)
                user.save()
                group, _ = Group.objects.get_or_create(name="DOCTOR")
                user.groups.add(group)
                doctor = doctor_form.save(commit=False)
                doctor.user = user
                doctor.save()
                messages.success(request, "Doctor created successfully.")
                return redirect("adm2_doctor_list")
            except Exception:
                logger.exception("adm2_doctor_add failed")
                messages.error(request, "Unable to create doctor right now.")
    else:
        user_form = AdminUserForm()
        doctor_form = DoctorForm()

    return render(
        request,
        "hospital/admin_add_doctor.html",
        {"userForm": user_form, "doctorForm": doctor_form},
    )


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def adm2_doctor_edit(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    user = doctor.user
    if request.method == "POST":
        user_form = AdminUserForm(request.POST, instance=user)
        doctor_form = DoctorForm(request.POST, request.FILES, instance=doctor)
        if user_form.is_valid() and doctor_form.is_valid():
            try:
                user = user_form.save(commit=False)
                if user_form.cleaned_data.get("password"):
                    user.set_password(user_form.cleaned_data["password"])
                user.save()
                doctor_form.save()
                messages.success(request, "Doctor updated successfully.")
                return redirect("adm2_doctor_list")
            except Exception:
                logger.exception("adm2_doctor_edit failed")
                messages.error(request, "Unable to update doctor right now.")
    else:
        user_form = AdminUserForm(instance=user)
        doctor_form = DoctorForm(instance=doctor)

    return render(
        request,
        "hospital/edit_doctor.html",
        {"userForm": user_form, "doctorForm": doctor_form},
    )


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def adm2_doctor_delete(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    try:
        if Appointment.objects.filter(doctor=doctor).exists():
            messages.error(
                request,
                "Cannot delete doctor because related appointments exist.",
            )
            return redirect("adm2_doctor_list")
        user = doctor.user
        doctor.delete()
        if user:
            user.delete()
        messages.success(request, "Doctor deleted successfully.")
    except (ProtectedError, IntegrityError):
        messages.error(request, "Unable to delete doctor because related records exist.")
    except Exception:
        logger.exception("adm2_doctor_delete failed")
        messages.error(request, "Unable to delete doctor right now.")
    return redirect("adm2_doctor_list")


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def adm2_doctor_approve(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    try:
        doctor.status = True
        doctor.save()
        messages.success(request, "Doctor approved successfully.")
    except Exception:
        logger.exception("adm2_doctor_approve failed")
        messages.error(request, "Unable to approve doctor right now.")
    return redirect("adm2_doctor_list")


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def adm2_patient_list(request):
    try:
        patients = Patient.objects.select_related("user")
        return render(
            request, "hospital/admin_view_patient.html", {"patients": patients}
        )
    except Exception:
        logger.exception("adm2_patient_list failed")
        messages.error(request, "Unable to load patients at this time.")
        return render(request, "hospital/admin_view_patient.html", {"patients": []})


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def adm2_patient_add(request):
    if request.method == "POST":
        user_form = AdminUserForm(request.POST)
        patient_form = PatientForm(request.POST, request.FILES)
        if user_form.is_valid() and patient_form.is_valid():
            try:
                if not user_form.cleaned_data.get("password"):
                    messages.error(request, "Password is required.")
                    return redirect("adm2_patient_add")
                user = user_form.save(commit=False)
                user.set_password(user.password)
                user.save()
                group, _ = Group.objects.get_or_create(name="PATIENT")
                user.groups.add(group)
                patient = patient_form.save(commit=False)
                patient.user = user
                patient.save()
                messages.success(request, "Patient created successfully.")
                return redirect("adm2_patient_list")
            except Exception:
                logger.exception("adm2_patient_add failed")
                messages.error(request, "Unable to create patient right now.")
    else:
        user_form = AdminUserForm()
        patient_form = PatientForm()

    return render(
        request,
        "hospital/admin_add_patient.html",
        {"userForm": user_form, "patientForm": patient_form},
    )


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def adm2_patient_edit(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    user = patient.user
    if request.method == "POST":
        user_form = AdminUserForm(request.POST, instance=user)
        patient_form = PatientForm(request.POST, request.FILES, instance=patient)
        if user_form.is_valid() and patient_form.is_valid():
            try:
                user = user_form.save(commit=False)
                if user_form.cleaned_data.get("password"):
                    user.set_password(user_form.cleaned_data["password"])
                user.save()
                patient_form.save()
                messages.success(request, "Patient updated successfully.")
                return redirect("adm2_patient_list")
            except Exception:
                logger.exception("adm2_patient_edit failed")
                messages.error(request, "Unable to update patient right now.")
    else:
        user_form = AdminUserForm(instance=user)
        patient_form = PatientForm(instance=patient)

    return render(
        request,
        "hospital/edit_patient.html",
        {"userForm": user_form, "patientForm": patient_form},
    )


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def adm2_patient_delete(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    try:
        if Appointment.objects.filter(patient=patient).exists():
            messages.error(
                request,
                "Cannot delete patient because related appointments exist.",
            )
            return redirect("adm2_patient_list")
        user = patient.user
        patient.delete()
        if user:
            user.delete()
        messages.success(request, "Patient deleted successfully.")
    except (ProtectedError, IntegrityError):
        messages.error(request, "Unable to delete patient because related records exist.")
    except Exception:
        logger.exception("adm2_patient_delete failed")
        messages.error(request, "Unable to delete patient right now.")
    return redirect("adm2_patient_list")


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def adm2_patient_admit(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    try:
        patient.status = True
        patient.save(update_fields=["status"])
        messages.success(request, "Patient admitted successfully.")
    except Exception:
        logger.exception("adm2_patient_admit failed")
        messages.error(request, "Unable to admit patient right now.")
    return redirect("adm2_patient_list")


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def adm2_appointment_list(request):
    try:
        appointments = Appointment.objects.select_related(
            "doctor__user", "patient__user"
        )
        return render(
            request,
            "hospital/admin_view_appointment.html",
            {"appointments": appointments},
        )
    except Exception:
        logger.exception("adm2_appointment_list failed")
        messages.error(request, "Unable to load appointments at this time.")
        return render(
            request, "hospital/admin_view_appointment.html", {"appointments": []}
        )


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def adm2_appointment_add(request):
    if request.method == "POST":
        form = AppointmentForm(request.POST)
        if form.is_valid():
            try:
                appointment = form.save(commit=False)
                appointment.created_by = request.user
                appointment.updated_by = request.user
                appointment.save()
                send_consultation_email(appointment, "appointment_created")
                messages.success(request, "Appointment created successfully.")
                return redirect("adm2_appointment_list")
            except Exception:
                logger.exception("adm2_appointment_add failed")
                messages.error(request, "Unable to create appointment right now.")
    else:
        form = AppointmentForm()

    return render(request, "hospital/admin_add_appointment.html", {"form": form})


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def adm2_appointment_edit(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    if request.method == "POST":
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            try:
                appointment = form.save(commit=False)
                appointment.updated_by = request.user
                appointment.save()
                messages.success(request, "Appointment updated successfully.")
                return redirect("adm2_appointment_list")
            except Exception:
                logger.exception("adm2_appointment_edit failed")
                messages.error(request, "Unable to update appointment right now.")
    else:
        form = AppointmentForm(instance=appointment)

    return render(
        request, "hospital/admin_update_appointment.html", {"form": form}
    )


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def adm2_appointment_delete(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    try:
        appointment.delete()
        messages.success(request, "Appointment deleted successfully.")
    except Exception:
        logger.exception("adm2_appointment_delete failed")
        messages.error(request, "Unable to delete appointment right now.")
    return redirect("adm2_appointment_list")


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def adm2_appointment_approve(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    try:
        appointment.status = "confirmed"
        appointment.save()
        send_consultation_email(appointment, "appointment_approved")
        messages.success(request, "Appointment approved successfully.")
    except Exception:
        logger.exception("adm2_appointment_approve failed")
        messages.error(request, "Unable to approve appointment right now.")
    return redirect("adm2_appointment_list")


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def adm2_appointment_reject(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    try:
        appointment.status = "cancelled"
        appointment.save()
        messages.success(request, "Appointment rejected successfully.")
    except Exception:
        logger.exception("adm2_appointment_reject failed")
        messages.error(request, "Unable to reject appointment right now.")
    return redirect("adm2_appointment_list")


def _build_invoice_context(patient, discharge, total_days):
    return {
        "name": patient.user.get_full_name(),
        "mobile": patient.mobile,
        "address": patient.address,
        "symptoms": patient.symptoms,
        "assignedDoctorName": discharge.doctor.user.get_full_name()
        if discharge.doctor and discharge.doctor.user
        else "N/A",
        "admitDate": discharge.admission_date.strftime("%Y-%m-%d"),
        "todayDate": discharge.discharge_date.strftime("%Y-%m-%d"),
        "day": total_days,
        "roomCharge": discharge.room_charge,
        "doctorFee": discharge.doctor_fee,
        "medicineCost": discharge.medicine_cost,
        "OtherCharge": discharge.other_charge,
        "total": discharge.total,
        "patientId": patient.id,
    }


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def adm2_discharge_patient(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    discharge_date = timezone.now().date()
    admission_date = patient.created_at.date() if patient.created_at else discharge_date
    total_days = max(1, (discharge_date - admission_date).days)

    if request.method == "POST":
        try:
            room_charge = float(request.POST.get("roomCharge", 0)) * total_days
            doctor_fee = float(request.POST.get("doctorFee", 0))
            medicine_cost = float(request.POST.get("medicineCost", 0))
            other_charge = float(request.POST.get("OtherCharge", 0))
            total = room_charge + doctor_fee + medicine_cost + other_charge

            discharge = DischargeDetails.objects.create(
                patient=patient,
                doctor=patient.assignedDoctorId,
                admission_date=admission_date,
                discharge_date=discharge_date,
                summary=f"Discharged due to recovery: {patient.symptoms}",
                room_charge=room_charge,
                doctor_fee=doctor_fee,
                medicine_cost=medicine_cost,
                other_charge=other_charge,
                total=total,
            )

            invoice = Invoice.objects.create(
                patient=patient,
                amount=total,
                created_by=request.user,
            )
            messages.success(request, "Patient discharged and invoice generated.")
            context = _build_invoice_context(patient, discharge, total_days)
            return render(request, "hospital/patient_final_bill.html", context)
        except Exception:
            logger.exception("adm2_discharge_patient failed")
            messages.error(request, "Unable to discharge patient right now.")

    context = {
        "name": patient.user.get_full_name(),
        "mobile": patient.mobile,
        "address": patient.address,
        "symptoms": patient.symptoms,
        "assignedDoctorName": patient.assignedDoctorId.user.get_full_name()
        if patient.assignedDoctorId
        else "N/A",
        "admitDate": admission_date,
        "todayDate": discharge_date,
        "day": total_days,
        "patientId": patient.id,
    }
    return render(request, "hospital/patient_generate_bill.html", context)


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def adm2_invoice_list(request):
    try:
        invoices = Invoice.objects.select_related("patient__user").order_by("-id")
        return render(
            request,
            "hospital/adm2_invoice_list.html",
            {"invoices": invoices},
        )
    except Exception:
        logger.exception("adm2_invoice_list failed")
        messages.error(request, "Unable to load invoices at this time.")
        return render(request, "hospital/adm2_invoice_list.html", {"invoices": []})


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def adm2_invoice_detail(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    discharge = DischargeDetails.objects.filter(patient=invoice.patient).last()
    total_days = 1
    if discharge:
        total_days = max(1, (discharge.discharge_date - discharge.admission_date).days)
    return render(
        request,
        "hospital/adm2_invoice_detail.html",
        {"invoice": invoice, "discharge": discharge, "total_days": total_days},
    )


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def adm2_download_pdf(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    discharge = DischargeDetails.objects.filter(patient=invoice.patient).last()
    if not discharge:
        messages.error(request, "No discharge record found for this invoice.")
        return redirect("adm2_invoice_list")

    total_days = max(1, (discharge.discharge_date - discharge.admission_date).days)
    context = _build_invoice_context(invoice.patient, discharge, total_days)
    pdf_bytes = render_invoice_pdf(context)
    if not pdf_bytes:
        messages.error(request, "Unable to generate PDF at this time.")
        return redirect("adm2_invoice_list")

    from django.http import HttpResponse

    response = HttpResponse(pdf_bytes, content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="invoice_{invoice.id}.pdf"'
    return response


@login_required(login_url="adminlogin")
@user_passes_test(is_admin)
def adm2_invoice_resend_email(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    discharge = DischargeDetails.objects.filter(patient=invoice.patient).last()
    if not discharge:
        messages.error(request, "No discharge record found for this invoice.")
        return redirect("adm2_invoice_list")

    total_days = max(1, (discharge.discharge_date - discharge.admission_date).days)
    context = _build_invoice_context(invoice.patient, discharge, total_days)
    pdf_bytes = render_invoice_pdf(context)
    if send_invoice_email(invoice, pdf_bytes):
        messages.success(request, "Invoice email sent.")
    else:
        messages.error(request, "Invoice email failed. See EmailLog for details.")
    return redirect("adm2_invoice_detail", pk=invoice.pk)
