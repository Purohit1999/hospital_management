# Django core
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseForbidden, Http404
from django.utils import timezone
from django.db.models import Q
from django.contrib import messages

# Authentication
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LogoutView
from django.contrib.auth.forms import AuthenticationForm

# CSRF & decorators
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

# PDF generation
from django.template.loader import get_template
from xhtml2pdf import pisa
import io

# Date/time
from datetime import datetime

# App-specific
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
@login_required
def patient_discharge_summary_view(request):
    patient = get_object_or_404(Patient, user=request.user)
    discharges = DischargeDetails.objects.filter(patient=patient).order_by('-discharge_date')

    # Add 'days_spent' field for each discharge object
    for discharge in discharges:
        discharge.days_spent = (discharge.discharge_date - discharge.admission_date).days or 1

    context = {
        'discharges': discharges,
        'patient': patient
    }

    return render(request, 'hospital/patient_discharge.html', context)

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
            return redirect('patient-appointment-list')
    else:
        form = AppointmentForm()
    return render(request, 'hospital/patient_book_appointment.html', {'form': form})


@login_required(login_url='patientlogin')
@user_passes_test(lambda u: u.groups.filter(name='PATIENT').exists())
def patient_appointment_list_view(request):
    patient = Patient.objects.get(user=request.user)
    appointments = Appointment.objects.filter(patient=patient).order_by('-date_time')
    return render(request, 'appointments/list.html', {'appointments': appointments})  # ✅ Correct path

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

@login_required
@user_passes_test(lambda u: u.is_superuser)
def generate_patient_bill_view(request, pk):
    patient = get_object_or_404(Patient, pk=pk)

    if hasattr(patient, 'dischargedetails'):
        messages.warning(request, "⚠️ Patient already discharged.")
        return redirect('admin-view-patient')

    admit_date = timezone.now().date()
    today = timezone.now().date()
    total_days = 1

    return render(request, 'hospital/patient_generate_bill.html', {
        'name': f"{patient.user.first_name} {patient.user.last_name}",
        'mobile': patient.mobile,
        'address': patient.address,
        'symptoms': patient.symptoms,
        'assignedDoctorName': patient.assignedDoctorId.user.get_full_name() if patient.assignedDoctorId else "N/A",
        'admitDate': admit_date,
        'todayDate': today,
        'day': total_days,
        'patientId': patient.id
    })

# Helper function to safely convert to float
def safe_float(value):
    try:
        return float(value)
    except (ValueError, TypeError):
        return 0.0


# View to discharge patient and show final bill in browser
@login_required
@user_passes_test(lambda u: u.is_superuser)
def discharge_patient_view(request, pk):
    patient = get_object_or_404(Patient, pk=pk)

    last_discharge = DischargeDetails.objects.filter(patient=patient).last()
    admit_date = last_discharge.admission_date if last_discharge else timezone.now().date()
    discharge_date = timezone.now().date()
    total_days = (discharge_date - admit_date).days or 1

    if request.method == 'POST':
        room_charge = safe_float(request.POST.get('roomCharge', 0)) * total_days
        doctor_fee = safe_float(request.POST.get('doctorFee', 0))
        medicine_cost = safe_float(request.POST.get('medicineCost', 0))
        other_charge = safe_float(request.POST.get('OtherCharge', 0))
        total = room_charge + doctor_fee + medicine_cost + other_charge

        DischargeDetails.objects.create(
            patient=patient,
            doctor=patient.assignedDoctorId,
            admission_date=admit_date,
            discharge_date=discharge_date,
            summary=f"Discharged due to recovery from symptoms: {patient.symptoms}",
            room_charge=room_charge,
            doctor_fee=doctor_fee,
            medicine_cost=medicine_cost,
            other_charge=other_charge,
            total=total
        )

        return render(request, 'hospital/patient_final_bill.html', {
            'name': f"{patient.user.first_name} {patient.user.last_name}",
            'mobile': patient.mobile,
            'address': patient.address,
            'symptoms': patient.symptoms,
            'assignedDoctorName': patient.assignedDoctorId.user.get_full_name() if patient.assignedDoctorId else "N/A",
            'admitDate': admit_date.strftime('%Y-%m-%d'),
            'todayDate': discharge_date.strftime('%Y-%m-%d'),
            'day': int(total_days),
            'roomCharge': room_charge,
            'doctorFee': doctor_fee,
            'medicineCost': medicine_cost,
            'OtherCharge': other_charge,
            'total': total,
            'patientId': patient.id
        })

    return render(request, 'hospital/patient_generate_bill.html', {
        'patient': patient,
        'admitDate': admit_date,
        'todayDate': discharge_date,
        'day': int(total_days),
    })


# View to download invoice PDF (admin only)
@login_required
@user_passes_test(lambda u: u.is_superuser)
def download_pdf_view(request, patientId):
    patient = get_object_or_404(Patient, pk=patientId)
    discharge = DischargeDetails.objects.filter(patient=patient).order_by('-discharge_date').first()

    if not discharge:
        messages.error(request, "Discharge details not found.")
        return redirect('admin-view-patient')

    # 🗓 Convert dates if they are strings
    admit_date = discharge.admission_date
    discharge_date = discharge.discharge_date

    if isinstance(admit_date, str):
        try:
            admit_date = datetime.strptime(admit_date, '%Y-%m-%d').date()
        except ValueError:
            messages.error(request, "Invalid admission date format.")
            return redirect('admin-view-patient')

    if isinstance(discharge_date, str):
        try:
            discharge_date = datetime.strptime(discharge_date, '%Y-%m-%d').date()
        except ValueError:
            messages.error(request, "Invalid discharge date format.")
            return redirect('admin-view-patient')

    # Calculate total stay duration
    try:
        total_days = (discharge_date - admit_date).days
        if total_days <= 0:
            total_days = 1
    except Exception as e:
        messages.error(request, f"Error calculating stay duration: {str(e)}")
        return redirect('admin-view-patient')

    # Context for rendering template
    context = {
        'name': f"{patient.user.first_name} {patient.user.last_name}",
        'mobile': str(patient.mobile),
        'address': str(patient.address),
        'symptoms': str(patient.symptoms),
        'assignedDoctorName': str(patient.assignedDoctorId.user.get_full_name() if patient.assignedDoctorId else "N/A"),
        'admitDate': admit_date.strftime('%Y-%m-%d'),
        'todayDate': discharge_date.strftime('%Y-%m-%d'),
        'day': int(total_days),
        'roomCharge': safe_float(discharge.room_charge),
        'doctorFee': safe_float(discharge.doctor_fee),
        'medicineCost': safe_float(discharge.medicine_cost),
        'OtherCharge': safe_float(discharge.other_charge),
        'total': safe_float(discharge.total),
        'patientId': int(patientId)
    }


    # 🖨️ Generate PDF
    template = get_template('hospital/patient_final_bill.html')
    html = template.render(context)
    result = io.BytesIO()
    pdf = pisa.pisaDocument(io.BytesIO(html.encode("UTF-8")), dest=result)

    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    else:
        messages.error(request, "Error generating PDF.")
        return redirect('admin-view-patient')