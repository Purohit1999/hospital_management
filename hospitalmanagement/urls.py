from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView
from hospital import views

urlpatterns = [
    # Admin Site
    path('admin/', admin.site.urls),

    # Home & Info Pages
    path('', views.home_view, name='home'),
    path('aboutus/', views.aboutus_view, name='aboutus'),
    path('contactus/', views.contactus_view, name='contactus'),

    # Role Clicks
    path('adminclick/', views.adminclick_view, name='adminclick'),
    path('doctorclick/', views.doctorclick_view, name='doctorclick'),
    path('patientclick/', views.patientclick_view, name='patientclick'),

    # Signup Views
    path('adminsignup/', views.admin_signup_view, name='adminsignup'),
    path('doctorsignup/', views.doctor_signup_view, name='doctorsignup'),
    path('patientsignup/', views.patient_signup_view, name='patientsignup'),

    # Login/Logout
    path('adminlogin/', LoginView.as_view(template_name='hospital/adminlogin.html'), name='adminlogin'),
    path('doctorlogin/', LoginView.as_view(template_name='hospital/doctorlogin.html'), name='doctorlogin'),
    path('patientlogin/', LoginView.as_view(template_name='hospital/patientlogin.html'), name='patientlogin'),
    path('afterlogin/', views.afterlogin_view, name='afterlogin'),
    path('logout/', LogoutView.as_view(template_name='hospital/index.html'), name='logout'),

    # Admin Dashboard
    path('admin-dashboard/', views.admin_dashboard_view, name='admin-dashboard'),

    # Admin - Doctor Management
    path('admin-view-doctor/', views.admin_view_doctor_view, name='admin-view-doctor'),
    path('admin-add-doctor/', views.admin_add_doctor_view, name='admin-add-doctor'),
    path('admin-approve-doctor/', views.admin_approve_doctor_view, name='admin-approve-doctor'),
    path('admin-view-doctor-specialisation/', views.admin_view_doctor_specialisation_view, name='admin-view-doctor-specialisation'),
    path('admin-doctor/', views.admin_doctor_view, name='admin-doctor'),

    path('approve-doctor/<int:pk>/', views.approve_doctor_view, name='approve-doctor'),
    path('reject-doctor/<int:pk>/', views.reject_doctor_view, name='reject-doctor'),
    path('edit-doctor/<int:pk>/', views.edit_doctor_view, name='edit-doctor'),
    path('update-doctor/<int:pk>/', views.update_doctor_view, name='update-doctor'),
    path('delete-doctor/<int:pk>/', views.delete_doctor_view, name='delete-doctor-from-hospital'),

    # Admin - Patient Management
    path('admin-patient/', views.admin_patient_view, name='admin-patient'),
    path('admin-view-patient/', views.admin_view_patient_view, name='admin-view-patient'),
    path('admin-add-patient/', views.admin_add_patient_view, name='admin-add-patient'),
    path('admin-approve-patient/', views.admin_approve_patient_view, name='admin-approve-patient'),
    path('admin-discharge-patient/', views.admin_discharge_patient_view, name='admin-discharge-patient'),

    path('edit-patient/<int:pk>/', views.edit_patient_view, name='edit-patient'),
    path('delete-patient/<int:pk>/', views.delete_patient_view, name='delete-patient'),
    path('discharge-patient/<int:pk>/', views.discharge_patient_view, name='discharge-patient'),

    # Admin - Appointment Management
    path('admin-appointment/', views.admin_appointment_view, name='admin-appointment'),
    path('admin-view-appointment/', views.admin_view_appointment, name='admin-view-appointment'),
    path('admin-add-appointment/', views.admin_add_appointment_view, name='admin-add-appointment'),
    path('admin-approve-appointment/', views.admin_approve_appointment_view, name='admin-approve-appointment'),

    # Public Appointment Access
    path('appointments/', views.list_appointments, name='appointments'),
    path('appointments/<int:pk>/', views.appointment_detail, name='appointment_detail'),
    path('patient-book-appointment/', views.patient_book_appointment_view, name='patient-book-appointment'),

    # Optional (uncomment if implemented)
    # path('approve-appointment/<int:pk>/', views.approve_appointment_view, name='approve-appointment'),
    # path('reject-appointment/<int:pk>/', views.reject_appointment_view, name='reject-appointment'),
    # path('download-bill/<int:pk>/', views.download_pdf_view, name='download-bill'),
]

# ✅ Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
