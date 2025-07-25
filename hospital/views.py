from django.shortcuts import render, get_object_or_404, redirect 
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from .models import Appointment, Doctor, Patient
from .forms import (
    AppointmentForm, 
    PatientUserForm, PatientForm, 
    DoctorUserForm, DoctorForm
)

# ---------- 🔹 HOME PAGE ----------
def home_view(request):
    return render(request, 'hospital/index.html')

# ---------- 🔹 Appointments ----------
def list_appointments(request):
    appointments = (
        Appointment.objects
        .select_related('patient', 'doctor')
        .filter(date_time__gte=timezone.now())
    )
    return render(request, 'appointments/list.html', {
        'appointments': appointments
    })

def appointment_detail(request, pk):
    appointment = get_object_or_404(
        Appointment.objects.select_related('patient', 'doctor'),
        pk=pk
    )
    return render(request, 'appointments/detail.html', {
        'appointment': appointment
    })

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


# ---------- 🔹 Static Pages ----------
def aboutus_view(request):
    return render(request, 'hospital/aboutus.html')

def contactus_view(request):
    return render(request, 'hospital/contactus.html')

# ---------- 🔹 Role Selection Pages ----------
def adminclick_view(request):
    return render(request, 'hospital/adminclick.html')

def doctorclick_view(request):
    return render(request, 'hospital/doctorclick.html')

def patientclick_view(request):
    return render(request, 'hospital/patientclick.html')

# ---------- 🔹 Signup Pages ----------
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

    return render(request, 'hospital/doctorsignup.html', {
        'userForm': user_form,
        'doctorForm': doctor_form
    })

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

    return render(request, 'hospital/patientsignup.html', {
        'userForm': user_form,
        'patientForm': patient_form
    })

# ---------- 🔹 Login + Redirect ----------
def afterlogin_view(request):
    if request.user.groups.filter(name='DOCTOR').exists():
        return redirect('doctor-dashboard')
    elif request.user.groups.filter(name='PATIENT').exists():
        return redirect('patient-dashboard')
    elif request.user.is_superuser:
        return redirect('admin-dashboard')
    else:
        return redirect('home')

# ---------- 🔹 Admin Features ----------
def admin_dashboard_view(request):
    return render(request, 'hospital/admin_dashboard.html')

def admin_doctor_view(request):
    return render(request, 'hospital/admin_doctor.html')

def admin_view_doctor_view(request):
    return render(request, 'hospital/admin_view_doctor.html')

def delete_doctor_from_hospital_view(request, pk):
    return redirect('admin-view-doctor')

def update_doctor_view(request, pk):
    return render(request, 'hospital/update_doctor.html', {'pk': pk})

def admin_add_doctor_view(request):
    return render(request, 'hospital/admin_add_doctor.html')

def admin_approve_doctor_view(request):
    return render(request, 'hospital/admin_approve_doctor.html')

def approve_doctor_view(request, pk):
    return redirect('admin-approve-doctor')

def reject_doctor_view(request, pk):
    return redirect('admin-approve-doctor')

def admin_view_doctor_specialisation_view(request):
    return render(request, 'hospital/admin_view_doctor_specialisation.html')

def admin_patient_view(request):
    return render(request, 'hospital/admin_patient.html')

def admin_view_patient_view(request):
    return render(request, 'hospital/admin_view_patient.html')

def delete_patient_from_hospital_view(request, pk):
    return redirect('admin-view-patient')

def update_patient_view(request, pk):
    return render(request, 'hospital/update_patient.html', {'pk': pk})

def admin_add_patient_view(request):
    return render(request, 'hospital/admin_add_patient.html')

def admin_approve_patient_view(request):
    return render(request, 'hospital/admin_approve_patient.html')

def approve_patient_view(request, pk):
    return redirect('admin-approve-patient')

def reject_patient_view(request, pk):
    return redirect('admin-approve-patient')

def admin_discharge_patient_view(request):
    return render(request, 'hospital/admin_discharge_patient.html')

def discharge_patient_view(request, pk):
    return redirect('admin-discharge-patient')

def download_pdf_view(request, pk):
    return render(request, 'hospital/download_pdf.html', {'pk': pk})

def admin_appointment_view(request):
    return render(request, 'hospital/admin_appointment.html')

def admin_view_appointment_view(request):
    return render(request, 'hospital/admin_view_appointment.html')

def admin_add_appointment_view(request):
    return render(request, 'hospital/admin_add_appointment.html')

def admin_approve_appointment_view(request):
    return render(request, 'hospital/admin_approve_appointment.html')

def approve_appointment_view(request, pk):
    return redirect('admin-approve-appointment')

def reject_appointment_view(request, pk):
    return redirect('admin-approve-appointment')

# ---------- 🔹 Doctor Views ----------
@login_required
def doctor_dashboard_view(request):
    doctor = Doctor.objects.filter(user=request.user).first()

    if not doctor:
        return redirect('doctor-wait-for-approval')

    appointments = Appointment.objects.filter(doctor=doctor).order_by('-date_time')
    patients = Patient.objects.filter(assignedDoctorId=doctor)

    return render(request, 'hospital/doctor_dashboard.html', {
        'doctor': doctor,
        'appointments': appointments,
        'patients': patients
    })

def search_view(request):
    return render(request, 'hospital/search.html')

def doctor_patient_view(request):
    return render(request, 'hospital/doctor_patient.html')

def doctor_view_patient_view(request):
    return render(request, 'hospital/doctor_view_patient.html')

def doctor_view_discharge_patient_view(request):
    return render(request, 'hospital/doctor_view_discharge_patient.html')

def doctor_appointment_view(request):
    return render(request, 'hospital/doctor_appointment.html')

def doctor_view_appointment_view(request):
    return render(request, 'hospital/doctor_view_appointment.html')

def doctor_delete_appointment_view(request):
    return redirect('doctor-view-appointment')

def delete_appointment_view(request, pk):
    return redirect('appointments')

# ---------- 🔹 Patient Views ----------
def patient_dashboard_view(request):
    return render(request, 'hospital/patient_dashboard.html')

def patient_appointment_view(request):
    return render(request, 'hospital/patient_appointment.html')

def patient_book_appointment_view(request):
    return render(request, 'hospital/patient_book_appointment.html')

def patient_view_appointment_view(request):
    return render(request, 'hospital/patient_view_appointment.html')

def patient_view_doctor_view(request):
    return render(request, 'hospital/patient_view_doctor.html')

def search_doctor_view(request):
    return render(request, 'hospital/searchdoctor.html')

def patient_discharge_view(request):
    return render(request, 'hospital/patient_discharge.html')
