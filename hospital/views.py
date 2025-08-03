from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import Group, User
from django.db.models import Q
from django.http import Http404
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LogoutView
from django.contrib.auth.forms import AuthenticationForm
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import Doctor, Patient, Appointment, DischargeDetails
from .forms import (
    AppointmentForm,
    PatientUserForm, PatientForm,
    DoctorUserForm, DoctorForm
)
# ---------------- CUSTOM LOGOUT ----------------
@method_decorator(csrf_exempt, name='dispatch')
class CustomLogoutView(LogoutView):
    def post(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

# ---------------- HOME & STATIC ----------------
def home_view(request):
    return render(request, 'hospital/index.html')

def aboutus_view(request):
    return render(request, 'hospital/aboutus.html')

def contactus_view(request):
    return render(request, 'hospital/contactus.html')

# ---------------- ROLE SELECTION ----------------
def adminclick_view(request):
    return render(request, 'hospital/adminclick.html')

def doctorclick_view(request):
    return render(request, 'hospital/doctorclick.html')

def patientclick_view(request):
    return render(request, 'hospital/patientclick.html')

# ---------------- SIGNUP ----------------
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
            doctor.status = False
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
            group, _ = Group.objects.get_or_create(name='PATIENT')
            user.groups.add(group)
            patient = patient_form.save(commit=False)
            patient.user = user
            patient.save()
            return redirect('patientlogin')
    else:
        user_form = PatientUserForm()
        patient_form = PatientForm()
    return render(request, 'hospital/patientsignup.html', {'userForm': user_form, 'patientForm': patient_form})

# ---------------- LOGIN REDIRECT ----------------
def afterlogin_view(request):
    if request.user.groups.filter(name='DOCTOR').exists():
        return redirect('doctor-dashboard')
    elif request.user.groups.filter(name='PATIENT').exists():
        return redirect('patient-dashboard')
    elif request.user.is_superuser:
        return redirect('admin-dashboard')
    return redirect('home')

# ---------------- DOCTOR LOGIN ----------------
def doctor_login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            try:
                doctor = Doctor.objects.get(user=user)
                if doctor.status:
                    login(request, user)
                    return redirect('doctor-dashboard')
                else:
                    messages.error(request, "❗Your doctor account is not approved yet.")
            except Doctor.DoesNotExist:
                messages.error(request, "❗Doctor profile not found.")
        else:
            messages.error(request, "❗Invalid username or password.")
    form = AuthenticationForm()
    return render(request, 'hospital/doctorlogin.html', {'form': form})

# ---------------- DOCTOR DASHBOARD ----------------
@login_required
def doctor_dashboard_view(request):
    doctor = get_object_or_404(Doctor, user=request.user)
    return render(request, 'hospital/doctor_dashboard.html', {'doctor': doctor})

@login_required
def doctor_view_patient_view(request):
    doctor = get_object_or_404(Doctor, user=request.user)
    patients = Patient.objects.filter(appointment__doctor=doctor).distinct()
    return render(request, 'hospital/doctor_view_patient.html', {'patients': patients})

@login_required
def doctor_view_appointment_view(request):
    doctor = get_object_or_404(Doctor, user=request.user)
    appointments = Appointment.objects.filter(doctor=doctor).select_related('patient__user')
    return render(request, 'hospital/doctor_view_appointment.html', {'appointments': appointments})

@login_required
@user_passes_test(lambda u: u.groups.filter(name='DOCTOR').exists())
def doctor_view_discharge_patient_view(request):
    doctor = Doctor.objects.get(user=request.user)
    discharged_patients = DischargeDetails.objects.filter(assignedDoctor=doctor)
    return render(request, 'hospital/doctor_view_discharge_patient.html', {
        'discharged_patients': discharged_patients
    })
def admin_approve_doctor_view(request):
    doctors = Doctor.objects.filter(status=False)
    return render(request, 'hospital/admin_approve_doctor.html', {'pending_doctors': doctors})

# ---------------- PATIENT DASHBOARD ----------------
@login_required
def patient_dashboard_view(request):
    patient = get_object_or_404(Patient, user=request.user)
    return render(request, 'hospital/patient_dashboard.html', {'patient': patient})

# ---------------- ADMIN DASHBOARD ----------------
@login_required
def admin_dashboard_view(request):
    context = {
        'pending_doctors': Doctor.objects.filter(status=False).count(),
        'pending_patients': Patient.objects.count(),
        'pending_appointments': Appointment.objects.filter(status='pending').count(),
        'recent_doctors': Doctor.objects.select_related('user').filter(status=True).order_by('-id')[:5],
        'recent_patients': Patient.objects.select_related('user').order_by('-id')[:5],
    }
    return render(request, 'hospital/admin_dashboard.html', context)

# ---------------- DOCTOR ADMIN ----------------
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
            group, _ = Group.objects.get_or_create(name='DOCTOR')
            user.groups.add(group)
            doctor = doctor_form.save(commit=False)
            doctor.user = user
            doctor.save()
            return redirect('admin-view-doctor')
    else:
        user_form = DoctorUserForm()
        doctor_form = DoctorForm()
    return render(request, 'hospital/admin_add_doctor.html', {'userForm': user_form, 'doctorForm': doctor_form})

def edit_doctor_view(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    user = doctor.user
    if request.method == 'POST':
        user_form = DoctorUserForm(request.POST, instance=user)
        doctor_form = DoctorForm(request.POST, request.FILES, instance=doctor)
        if user_form.is_valid() and doctor_form.is_valid():
            user_form.save()
            doctor_form.save()
            return redirect('admin-view-doctor')
    else:
        user_form = DoctorUserForm(instance=user)
        doctor_form = DoctorForm(instance=doctor)
    return render(request, 'hospital/edit_doctor.html', {
        'userForm': user_form,
        'doctorForm': doctor_form
    })

# ---------------- PATIENT ADMIN ----------------
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

def approve_patient_view(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    patient.status = True
    patient.save()
    return redirect('admin-approve-patient')

def reject_patient_view(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    user = patient.user
    patient.delete()
    user.delete()
    return redirect('admin-approve-patient')

# ---------------- DISCHARGE PATIENT ----------------
def discharge_patient_view(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    patient.status = True
    patient.save()
    return redirect('admin-dashboard')

def admin_approve_patient_view(request):
    patients = Patient.objects.filter(dischargedetails__isnull=True)
    return render(request, 'hospital/admin_approve_patient.html', {'patients': patients})

def admin_discharge_patient_view(request):
    patients = Patient.objects.filter(status=True, dischargedetails__isnull=True).select_related('user')
    return render(request, 'hospital/admin_discharge_patient.html', {'patients': patients})

# ---------------- APPOINTMENTS ----------------

@login_required(login_url='patientlogin')
@user_passes_test(lambda u: u.groups.filter(name='PATIENT').exists())
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
            return redirect('patient-appointment-list')  # Redirect to the new view
    else:
        form = AppointmentForm()
    return render(request, 'hospital/patient_book_appointment.html', {'form': form})


@login_required(login_url='patientlogin')
@user_passes_test(lambda u: u.groups.filter(name='PATIENT').exists())
def patient_appointment_list_view(request):
    patient = Patient.objects.get(user=request.user)
    appointments = Appointment.objects.filter(patient=patient).order_by('-date_time')
    return render(request, 'hospital/patient_appointment_list.html', {'appointments': appointments})


# ---------------- ADMIN / OTHER VIEWS ----------------

def list_appointments(request):
    appointments = Appointment.objects.select_related('patient', 'doctor').filter(date_time__gte=timezone.now())
    return render(request, 'appointments/list.html', {'appointments': appointments})


def appointment_detail(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    return render(request, 'appointments/detail.html', {'appointment': appointment})


def admin_view_appointment(request):
    appointments = Appointment.objects.select_related('doctor__user', 'patient__user').all()
    return render(request, 'hospital/admin_view_appointment.html', {'appointments': appointments})


def admin_appointment_view(request):
    return render(request, 'hospital/admin_appointment.html')


def admin_approve_appointment_view(request):
    return render(request, 'hospital/admin_approve_appointment.html')

# ---------------- SPECIALISATION VIEW ----------------
def admin_view_doctor_specialisation(request):
    doctors = Doctor.objects.select_related('user').filter(status=True)
    return render(request, 'hospital/admin_view_doctor_specialisation.html', {'doctors': doctors})

def edit_doctor_view(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    user = doctor.user
    if request.method == 'POST':
        user_form = DoctorUserForm(request.POST, instance=user)
        doctor_form = DoctorForm(request.POST, request.FILES, instance=doctor)
        if user_form.is_valid() and doctor_form.is_valid():
            user_form.save()
            doctor_form.save()
            return redirect('admin-view-doctor')
    else:
        user_form = DoctorUserForm(instance=user)
        doctor_form = DoctorForm(instance=doctor)
    return render(request, 'hospital/edit_doctor.html', {
        'userForm': user_form,
        'doctorForm': doctor_form
    })

def admin_add_appointment_view(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.created_by = request.user
            appointment.updated_by = request.user
            appointment.save()
            messages.success(request, "Appointment added successfully.")
            return redirect('admin-view-appointment')
    else:
        form = AppointmentForm()
    return render(request, 'hospital/admin_add_appointment.html', {'form': form})

@login_required(login_url='doctorlogin')
@user_passes_test(lambda u: u.groups.filter(name='DOCTOR').exists())
def doctor_view_discharge_patient_view(request):
    doctor = Doctor.objects.get(user=request.user)
    discharged_patients = DischargeDetails.objects.filter(doctor=doctor)
    return render(request, 'hospital/doctor_view_discharge_patient.html', {
        'discharged_patients': discharged_patients
    })

def approve_doctor_view(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    doctor.status = True
    doctor.save()
    messages.success(request, "Doctor approved successfully.")
    return redirect('admin-approve-doctor')

def reject_doctor_view(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    user = doctor.user
    doctor.delete()
    if user:
        user.delete()
    messages.success(request, "Doctor has been rejected and removed.")
    return redirect('admin-approve-doctor')
def update_doctor_view(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    user = doctor.user
    if request.method == 'POST':
        user_form = DoctorUserForm(request.POST, instance=user)
        doctor_form = DoctorForm(request.POST, request.FILES, instance=doctor)
        if user_form.is_valid() and doctor_form.is_valid():
            user_form.save()
            doctor_form.save()
            return redirect('admin-view-doctor')
    else:
        user_form = DoctorUserForm(instance=user)
        doctor_form = DoctorForm(instance=doctor)
    return render(request, 'hospital/edit_doctor.html', {
        'userForm': user_form,
        'doctorForm': doctor_form
    })
def delete_doctor_view(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    user = doctor.user
    doctor.delete()
    if user:
        user.delete()
    return redirect('admin-view-doctor')

@login_required(login_url='doctorlogin')
@user_passes_test(lambda u: u.groups.filter(name='DOCTOR').exists())
def doctor_search_patient_view(request):
    query = request.GET.get('query', '')
    doctor = Doctor.objects.get(user=request.user)

    patients = Patient.objects.filter(
        assignedDoctorId=doctor
    ).filter(
        Q(user__first_name__icontains=query) |
        Q(user__last_name__icontains=query) |
        Q(symptoms__icontains=query)
    ).distinct()

    return render(request, 'hospital/doctor_view_patient.html', {'patients': patients})
