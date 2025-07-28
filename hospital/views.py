from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from django.db.models import Q
from django.http import Http404
from django.contrib import messages

from .models import Doctor, Patient, Appointment, DischargeDetails
from .forms import (
    AppointmentForm,
    PatientUserForm, PatientForm,
    DoctorUserForm, DoctorForm
)

# ---------- 🔹 HOME & STATIC PAGES ----------
def home_view(request):
    return render(request, 'hospital/index.html')

def aboutus_view(request):
    return render(request, 'hospital/aboutus.html')

def contactus_view(request):
    return render(request, 'hospital/contactus.html')

# ---------- 🔹 ROLE SELECTION ----------
def adminclick_view(request):
    return render(request, 'hospital/adminclick.html')

def doctorclick_view(request):
    return render(request, 'hospital/doctorclick.html')

def patientclick_view(request):
    return render(request, 'hospital/patientclick.html')

# ---------- 🔹 SIGNUP VIEWS ----------
def admin_signup_view(request):
    return render(request, 'hospital/adminsignup.html')

def doctor_signup_view(request):
    if request.method == 'POST':
        user_form = DoctorUserForm(request.POST)
        doctor_form = DoctorForm(request.POST, request.FILES)
        if user_form.is_valid() and doctor_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user.password)
            user.save()
            doctor_group, _ = Group.objects.get_or_create(name='DOCTOR')
            user.groups.add(doctor_group)
            doctor = doctor_form.save(commit=False)
            doctor.user = user
            doctor.save()
            return redirect('doctorlogin')
    else:
        user_form = DoctorUserForm()
        doctor_form = DoctorForm()
    return render(request, 'hospital/doctorsignup.html', {'userForm': user_form, 'doctorForm': doctor_form})

def patient_signup_view(request):
    if request.method == 'POST':
        user_form = PatientUserForm(request.POST)
        patient_form = PatientForm(request.POST, request.FILES)
        if user_form.is_valid() and patient_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user.password)
            user.save()
            patient_group, _ = Group.objects.get_or_create(name='PATIENT')
            user.groups.add(patient_group)
            patient = patient_form.save(commit=False)
            patient.user = user
            patient.save()
            return redirect('patientlogin')
    else:
        user_form = PatientUserForm()
        patient_form = PatientForm()
    return render(request, 'hospital/patientsignup.html', {'userForm': user_form, 'patientForm': patient_form})

# ---------- 🔹 LOGIN REDIRECT ----------
def afterlogin_view(request):
    if request.user.groups.filter(name='DOCTOR').exists():
        return redirect('doctor-dashboard')
    elif request.user.groups.filter(name='PATIENT').exists():
        return redirect('patient-dashboard')
    elif request.user.is_superuser:
        return redirect('admin-dashboard')
    return redirect('home')

# ---------- 🔹 ADMIN DASHBOARD ----------
def admin_dashboard_view(request):
    context = {
        'pending_doctors': Doctor.objects.filter(status=False).count(),
        'pending_patients': Patient.objects.count(),
        'pending_appointments': Appointment.objects.filter(status='pending').count(),
        'recent_doctors': Doctor.objects.select_related('user').order_by('-id')[:5],
        'recent_patients': Patient.objects.select_related('user').order_by('-id')[:5],
    }
    return render(request, 'hospital/admin_dashboard.html', context)

# ---------- 🔹 DOCTOR ADMIN ----------
def admin_doctor_view(request):
    return render(request, 'hospital/admin_doctor.html')

def admin_view_doctor_view(request):
    doctors = Doctor.objects.select_related('user').all()
    return render(request, 'hospital/admin_view_doctor.html', {'doctors': doctors})

def admin_add_doctor_view(request):
    if request.method == 'POST':
        user_form = DoctorUserForm(request.POST)
        doctor_form = DoctorForm(request.POST, request.FILES)
        if user_form.is_valid() and doctor_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user.password)
            user.save()
            doctor_group, _ = Group.objects.get_or_create(name='DOCTOR')
            user.groups.add(doctor_group)
            doctor = doctor_form.save(commit=False)
            doctor.user = user
            doctor.save()
            return redirect('admin-view-doctor')
    else:
        user_form = DoctorUserForm()
        doctor_form = DoctorForm()
    return render(request, 'hospital/admin_add_doctor.html', {'userForm': user_form, 'doctorForm': doctor_form})

def admin_approve_doctor_view(request):
    doctors = Doctor.objects.filter(status=False)
    return render(request, 'hospital/admin_approve_doctor.html', {'pending_doctors': doctors})

def admin_view_doctor_specialisation_view(request):
    return render(request, 'hospital/admin_view_doctor_specialisation.html')

def approve_doctor_view(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    doctor.status = True
    doctor.save()
    return redirect('admin-approve-doctor')

def reject_doctor_view(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    user = doctor.user
    doctor.delete()
    if user:
        user.delete()
    messages.success(request, "Doctor has been rejected and removed.")
    return redirect('admin-approve-doctor')

def delete_doctor_view(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    user = doctor.user
    doctor.delete()
    if user:
        user.delete()
    return redirect('admin-view-doctor')

def edit_doctor(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    if doctor.user is None:
        raise Http404("Doctor user not found")
    user_form = DoctorUserForm(request.POST or None, instance=doctor.user)
    doctor_form = DoctorForm(request.POST or None, request.FILES or None, instance=doctor)
    if request.method == 'POST':
        if user_form.is_valid() and doctor_form.is_valid():
            user_form.save()
            doctor_form.save()
            return redirect('admin-view-doctor')
    return render(request, 'hospital/edit_doctor.html', {'userForm': user_form, 'doctorForm': doctor_form, 'doctor': doctor})

# ---------- 🔹 PATIENT ADMIN ----------
def admin_patient_view(request):
    return render(request, 'hospital/admin_patient.html')

def admin_view_patient_view(request):
    patients = Patient.objects.select_related('user').all()
    return render(request, 'hospital/admin_view_patient.html', {'patients': patients})

def admin_add_patient_view(request):
    if request.method == 'POST':
        user_form = PatientUserForm(request.POST)
        patient_form = PatientForm(request.POST, request.FILES)
        if user_form.is_valid() and patient_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user.password)
            user.save()
            group, _ = Group.objects.get_or_create(name='PATIENT')
            user.groups.add(group)
            patient = patient_form.save(commit=False)
            patient.user = user
            patient.save()
            return redirect('admin-view-patient')
    else:
        user_form = PatientUserForm()
        patient_form = PatientForm()
    return render(request, 'hospital/admin_add_patient.html', {'userForm': user_form, 'patientForm': patient_form})

def edit_patient_view(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    user = patient.user
    if request.method == 'POST':
        user_form = PatientUserForm(request.POST, instance=user)
        patient_form = PatientForm(request.POST, request.FILES, instance=patient)
        if user_form.is_valid() and patient_form.is_valid():
            user_form.save()
            patient_form.save()
            return redirect('admin-view-patient')
    else:
        user_form = PatientUserForm(instance=user)
        patient_form = PatientForm(instance=patient)
    return render(request, 'hospital/edit_patient.html', {'userForm': user_form, 'patientForm': patient_form})

def delete_patient_view(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    user = patient.user
    patient.delete()
    if user:
        user.delete()
    return redirect('admin-view-patient')

# ---------- 🔹 DISCHARGE PATIENT ----------
def discharge_patient_view(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if hasattr(patient, 'dischargedetails'):
        messages.warning(request, "Patient is already discharged.")
    else:
        DischargeDetails.objects.create(
            patient=patient,
            doctor=patient.assignedDoctorId,
            admission_date=timezone.now().date(),
            discharge_date=timezone.now().date(),
            summary="Auto-discharged by admin.",
            room_charge=0.0,
            doctor_fee=0.0,
            medicine_cost=0.0,
            other_charge=0.0,
            total=0.0
        )
        messages.success(request, "Patient has been discharged.")
    return redirect('admin-dashboard')

# ---------- 🔹 APPOINTMENTS ----------
@login_required
def patient_book_appointment_view(request):
    patient = Patient.objects.filter(user=request.user).first()
    if not patient:
        return redirect('patient-dashboard')
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = patient
            appointment.created_by = request.user
            appointment.updated_by = request.user
            appointment.save()
            return redirect('patient-view-appointment')
    else:
        form = AppointmentForm()
    return render(request, 'hospital/patient_book_appointment.html', {'form': form})

def list_appointments(request):
    appointments = Appointment.objects.select_related('patient', 'doctor').filter(date_time__gte=timezone.now())
    return render(request, 'appointments/list.html', {'appointments': appointments})

def appointment_detail(request, pk):
    appointment = get_object_or_404(Appointment.objects.select_related('patient', 'doctor'), pk=pk)
    return render(request, 'appointments/detail.html', {'appointment': appointment})
def admin_approve_patient_view(request):
    patients = Patient.objects.filter(dischargedetails__isnull=True)  # Only admitted
    return render(request, 'hospital/admin_approve_patient.html', {'patients': patients})
def admin_discharge_patient_view(request):
    patients = Patient.objects.filter(status=True, dischargedetails__isnull=True)
    return render(request, 'hospital/admin_discharge_patient.html', {'patients': patients})
def admin_appointment_view(request):
    return render(request, 'hospital/admin_appointment.html')
def admin_view_appointment(request):
    return render(request, 'hospital/admin_view_appointment.html')  # Or whichever template you intend
def admin_add_appointment_view(request):
    return render(request, 'hospital/admin_add_appointment.html')
def admin_approve_appointment_view(request):
    return render(request, 'hospital/admin_approve_appointment.html')
def update_doctor_view(request, pk):
    pass
