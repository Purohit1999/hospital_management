from django.contrib import admin
from .models import (
    Doctor,
    Patient,
    DischargeDetails,
    Appointment,
    Prescription,
    Invoice,
    Feedback
)

# Doctor Admin
@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('name', 'specialization', 'contact_number', 'created_at')
    search_fields = ('name', 'specialization')


# Patient Admin
@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('user_full_name', 'mobile', 'assignedDoctorId', 'created_at')
    search_fields = ('user__first_name', 'user__last_name', 'mobile')

    def user_full_name(self, obj):
        return obj.user.get_full_name()
    user_full_name.short_description = 'Patient Name'


# DischargeDetails Admin
@admin.register(DischargeDetails)
class DischargeAdmin(admin.ModelAdmin):
    list_display = ('patient', 'admission_date', 'discharge_date', 'total')
    list_filter = ('discharge_date', 'doctor')
    search_fields = ('patient__user__first_name', 'patient__user__last_name')


# Appointment Admin
@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'date_time', 'status')
    list_filter = ('status', 'doctor')
    date_hierarchy = 'date_time'
    search_fields = ('patient__user__first_name', 'doctor__name')


# Prescription Admin
@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ('appointment', 'date_issued')
    search_fields = ('appointment__patient__user__first_name',)


# Invoice Admin
@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('patient', 'issued_date', 'amount', 'paid')
    list_filter = ('paid',)
    search_fields = ('patient__user__first_name',)


# Feedback Admin
@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('appointment', 'rating', 'submitted_at')
    list_filter = ('rating',)
    search_fields = ('appointment__patient__user__first_name',)
