from django import forms
from django.utils import timezone
from django.contrib.auth.models import User
from .models import Appointment, Patient


# ---------- 🔹 Appointment Form ----------
class AppointmentForm(forms.ModelForm):
    """
    Form to schedule or update an appointment.
    Includes validation for future date and Bootstrap-friendly widgets.
    """
    date_time = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={
            'type': 'datetime-local',
            'class': 'form-control',
            'placeholder': 'Select appointment date and time'
        }),
        label="Appointment Date & Time"
    )

    status = forms.ChoiceField(
        choices=Appointment.STATUS_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-select'
        }),
        label="Appointment Status"
    )

    class Meta:
        model = Appointment
        fields = ['patient', 'doctor', 'date_time', 'status']
        widgets = {
            'patient': forms.Select(attrs={'class': 'form-select'}),
            'doctor': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean_date_time(self):
        """
        Ensure the date_time is not in the past.
        """
        dt = self.cleaned_data['date_time']
        if dt < timezone.now():
            raise forms.ValidationError("Appointment date must be in the future.")
        return dt


# ---------- 🔹 Patient Registration Forms ----------

class PatientUserForm(forms.ModelForm):
    """
    Form for creating a User instance (for Patient).
    """
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password']
        widgets = {
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }


class PatientForm(forms.ModelForm):
    """
    Form for creating a Patient profile.
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
from .models import Doctor  # Add this if not already present

# ---------- 🔹 Doctor Registration Forms ----------
class DoctorUserForm(forms.ModelForm):
    """
    Form for creating a User instance (for Doctor).
    """
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password']
        widgets = {
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }


class DoctorForm(forms.ModelForm):
    """
    Form for creating a Doctor profile.
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
