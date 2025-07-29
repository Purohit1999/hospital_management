from django import forms
from django.utils import timezone
from django.contrib.auth.models import User
from .models import Appointment, Patient, Doctor

# ---------- 🔹 User Edit Form (Admin Edit Only) ----------
class UserForm(forms.ModelForm):
    """
    Form for editing user info (by admin or staff).
    """
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }


# ---------- 🔹 Appointment Form ----------
class AppointmentForm(forms.ModelForm):
    """
    Used by patients to book an appointment.
    """
    date_time = forms.DateTimeField(
        input_formats=['%Y-%m-%dT%H:%M'],
        widget=forms.DateTimeInput(attrs={
            'type': 'datetime-local',
            'class': 'form-control',
            'placeholder': 'Select appointment date and time'
        }),
        label="Appointment Date & Time"
    )

    description = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Describe your symptoms or reason for appointment'
        }),
        label="Reason / Description"
    )

    class Meta:
        model = Appointment
        fields = ['description', 'doctor', 'date_time']
        widgets = {
            'doctor': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean_date_time(self):
        dt = self.cleaned_data.get('date_time')
        if dt and dt < timezone.now():
            raise forms.ValidationError("Appointment date must be in the future.")
        return dt


# ---------- 🔹 Patient User Form ----------
class PatientUserForm(forms.ModelForm):
    """
    Creates a new User for Patient.
    """
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
        }


# ---------- 🔹 Patient Profile Form ----------
class PatientForm(forms.ModelForm):
    """
    Creates or updates Patient profile.
    """
    class Meta:
        model = Patient
        fields = ['address', 'mobile', 'symptoms', 'profile_pic', 'assignedDoctorId']
        widgets = {
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'mobile': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone (optional)'}),
            'symptoms': forms.TextInput(attrs={'class': 'form-control'}),
            'profile_pic': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'assignedDoctorId': forms.Select(attrs={'class': 'form-select'}),
        }


# ---------- 🔹 Doctor User Form ----------
class DoctorUserForm(forms.ModelForm):
    """
    Creates a new User for Doctor.
    """
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
        }


# ---------- 🔹 Doctor Profile Form ----------
class DoctorForm(forms.ModelForm):
    """
    Creates or updates Doctor profile.
    """
    class Meta:
        model = Doctor
        fields = ['department', 'address', 'mobile', 'profile_pic']
        widgets = {
            'department': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'mobile': forms.TextInput(attrs={'class': 'form-control'}),
            'profile_pic': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
