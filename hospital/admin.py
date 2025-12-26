from django.contrib import admin
from .models import (
    Doctor,
    Patient,
    DischargeDetails,
    Appointment,
    Prescription,
    Invoice,
    Feedback,
    ConsultationRequest,
)

# ------------------------------------------------------------
# Doctor Admin
# ------------------------------------------------------------
@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('doctor_name', 'department', 'mobile', 'status', 'created_at')
    search_fields = ('user__first_name', 'user__last_name', 'department')
    list_filter = ('status', 'department')
    ordering = ('-created_at',)

    def doctor_name(self, obj):
        return obj.user.get_full_name() if obj.user else 'Unassigned'
    doctor_name.short_description = 'Doctor Name'


# ------------------------------------------------------------
# Patient Admin
# ------------------------------------------------------------
@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('patient_name', 'mobile', 'assignedDoctor', 'created_at')
    search_fields = ('user__first_name', 'user__last_name', 'mobile')
    list_filter = ('created_at',)
    ordering = ('-created_at',)

    def patient_name(self, obj):
        return obj.user.get_full_name() if obj.user else 'Unassigned'
    patient_name.short_description = 'Patient Name'

    def assignedDoctor(self, obj):
        return obj.assignedDoctorId.user.get_full_name() if obj.assignedDoctorId and obj.assignedDoctorId.user else 'Not Assigned'
    assignedDoctor.short_description = 'Assigned Doctor'


# ------------------------------------------------------------
# DischargeDetails Admin
# ------------------------------------------------------------
@admin.register(DischargeDetails)
class DischargeDetailsAdmin(admin.ModelAdmin):
    list_display = ('patient_name', 'doctor_name', 'admission_date', 'discharge_date', 'total')
    list_filter = ('discharge_date', 'doctor')
    search_fields = ('patient__user__first_name', 'patient__user__last_name')
    ordering = ('-discharge_date',)

    def patient_name(self, obj):
        return obj.patient.user.get_full_name() if obj.patient and obj.patient.user else 'Unknown Patient'
    patient_name.short_description = 'Patient'

    def doctor_name(self, obj):
        return obj.doctor.user.get_full_name() if obj.doctor and obj.doctor.user else 'Unknown Doctor'
    doctor_name.short_description = 'Doctor'


# ------------------------------------------------------------
# Appointment Admin
# ------------------------------------------------------------
@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient_name', 'doctor_name', 'date_time', 'status')
    list_filter = ('status', 'doctor')
    search_fields = ('patient__user__first_name', 'doctor__user__first_name')
    date_hierarchy = 'date_time'
    ordering = ('-date_time',)

    def patient_name(self, obj):
        return obj.patient.user.get_full_name() if obj.patient and obj.patient.user else 'Unknown Patient'
    patient_name.short_description = 'Patient'

    def doctor_name(self, obj):
        return obj.doctor.user.get_full_name() if obj.doctor and obj.doctor.user else 'Unknown Doctor'
    doctor_name.short_description = 'Doctor'


# ------------------------------------------------------------
# Prescription Admin
# ------------------------------------------------------------
@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ('appointment_info', 'date_issued')
    search_fields = ('appointment__patient__user__first_name', 'appointment__doctor__user__first_name')
    ordering = ('-date_issued',)

    def appointment_info(self, obj):
        if obj.appointment and obj.appointment.patient and obj.appointment.patient.user:
            return f"{obj.appointment.patient.user.get_full_name()} - {obj.appointment.date_time.strftime('%Y-%m-%d %H:%M')}"
        return "Unknown"
    appointment_info.short_description = 'Appointment'


# ------------------------------------------------------------
# Invoice Admin
# ------------------------------------------------------------
@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('patient_name', 'issued_date', 'amount', 'paid')
    list_filter = ('paid', 'issued_date')
    search_fields = ('patient__user__first_name', 'patient__user__last_name')
    ordering = ('-issued_date',)

    def patient_name(self, obj):
        return obj.patient.user.get_full_name() if obj.patient and obj.patient.user else 'Unknown'
    patient_name.short_description = 'Patient'


# ------------------------------------------------------------
# Feedback Admin
# ------------------------------------------------------------
@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('appointment_info', 'rating', 'submitted_at')
    list_filter = ('rating',)
    search_fields = ('appointment__patient__user__first_name', 'appointment__doctor__user__first_name')
    ordering = ('-submitted_at',)

    def appointment_info(self, obj):
        if obj.appointment and obj.appointment.patient and obj.appointment.patient.user:
            return f"{obj.appointment.patient.user.get_full_name()} ({obj.rating}/5)"
        return "Unknown"
    appointment_info.short_description = 'Feedback From'


# ------------------------------------------------------------
# Consultation Request Admin
# ------------------------------------------------------------
@admin.register(ConsultationRequest)
class ConsultationRequestAdmin(admin.ModelAdmin):
    list_display = (
        "full_name",
        "email",
        "phone",
        "preferred_date",
        "preferred_time",
        "status",
        "created_at",
    )
    search_fields = ("full_name", "email", "phone", "message")
    list_filter = ("status", "preferred_date", "created_at")
