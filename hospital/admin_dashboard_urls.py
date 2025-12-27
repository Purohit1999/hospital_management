from django.urls import path

from . import admin_dashboard_views as views

urlpatterns = [
    path("doctors/", views.adm2_doctor_list, name="adm2_doctor_list"),
    path("doctors/add/", views.adm2_doctor_add, name="adm2_doctor_add"),
    path("doctors/<int:pk>/edit/", views.adm2_doctor_edit, name="adm2_doctor_edit"),
    path("doctors/<int:pk>/delete/", views.adm2_doctor_delete, name="adm2_doctor_delete"),
    path("doctors/<int:pk>/approve/", views.adm2_doctor_approve, name="adm2_doctor_approve"),

    path("patients/", views.adm2_patient_list, name="adm2_patient_list"),
    path("patients/add/", views.adm2_patient_add, name="adm2_patient_add"),
    path("patients/<int:pk>/edit/", views.adm2_patient_edit, name="adm2_patient_edit"),
    path("patients/<int:pk>/delete/", views.adm2_patient_delete, name="adm2_patient_delete"),
    path("patients/<int:pk>/admit/", views.adm2_patient_admit, name="adm2_patient_admit"),

    path("appointments/", views.adm2_appointment_list, name="adm2_appointment_list"),
    path("appointments/add/", views.adm2_appointment_add, name="adm2_appointment_add"),
    path("appointments/<int:pk>/edit/", views.adm2_appointment_edit, name="adm2_appointment_edit"),
    path("appointments/<int:pk>/delete/", views.adm2_appointment_delete, name="adm2_appointment_delete"),
    path("appointments/<int:pk>/approve/", views.adm2_appointment_approve, name="adm2_appointment_approve"),
    path("appointments/<int:pk>/reject/", views.adm2_appointment_reject, name="adm2_appointment_reject"),

    path("discharge/<int:pk>/", views.adm2_discharge_patient, name="adm2_discharge_patient"),

    path("invoices/", views.adm2_invoice_list, name="adm2_invoice_list"),
    path("invoices/<int:pk>/", views.adm2_invoice_detail, name="adm2_invoice_detail"),
    path("invoices/<int:pk>/download/", views.adm2_download_pdf, name="adm2_download_pdf"),
    path("invoices/<int:pk>/resend-email/", views.adm2_invoice_resend_email, name="adm2_invoice_resend_email"),
]
