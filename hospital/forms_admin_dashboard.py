from django import forms
from django.contrib.auth.models import User

from .models import Doctor, Patient, Appointment, DischargeDetails


class AdminUserForm(forms.ModelForm):
    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={"class": "form-control"}),
    )
    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )

    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email", "password"]
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "username": forms.TextInput(attrs={"class": "form-control"}),
        }


class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ["department", "mobile", "address", "profile_pic"]
        widgets = {
            "department": forms.TextInput(attrs={"class": "form-control"}),
            "mobile": forms.TextInput(attrs={"class": "form-control"}),
            "address": forms.TextInput(attrs={"class": "form-control"}),
            "profile_pic": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ["address", "mobile", "symptoms", "profile_pic", "assignedDoctorId"]
        widgets = {
            "address": forms.TextInput(attrs={"class": "form-control"}),
            "mobile": forms.TextInput(attrs={"class": "form-control"}),
            "symptoms": forms.TextInput(attrs={"class": "form-control"}),
            "profile_pic": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "assignedDoctorId": forms.Select(attrs={"class": "form-control"}),
        }


class AppointmentForm(forms.ModelForm):
    date_time = forms.DateTimeField(
        input_formats=["%Y-%m-%dT%H:%M"],
        widget=forms.DateTimeInput(
            attrs={"type": "datetime-local", "class": "form-control"}
        ),
    )

    class Meta:
        model = Appointment
        fields = ["doctor", "patient", "date_time", "description", "status"]
        widgets = {
            "doctor": forms.Select(attrs={"class": "form-control"}),
            "patient": forms.Select(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "status": forms.Select(attrs={"class": "form-control"}),
        }


class DischargeForm(forms.ModelForm):
    class Meta:
        model = DischargeDetails
        fields = [
            "admission_date",
            "discharge_date",
            "room_charge",
            "doctor_fee",
            "medicine_cost",
            "other_charge",
            "summary",
        ]
        widgets = {
            "admission_date": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
            "discharge_date": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
            "room_charge": forms.NumberInput(attrs={"class": "form-control"}),
            "doctor_fee": forms.NumberInput(attrs={"class": "form-control"}),
            "medicine_cost": forms.NumberInput(attrs={"class": "form-control"}),
            "other_charge": forms.NumberInput(attrs={"class": "form-control"}),
            "summary": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }
