from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from hospital import views

urlpatterns = [
    # Admin site
    path('admin/', admin.site.urls),

    # Home and Static Pages
    path('', views.home_view, name='home'),
    path('aboutus/', views.aboutus_view, name='aboutus'),
    path('contactus/', views.contactus_view, name='contactus'),

    # Appointment Management
    path('appointments/', views.list_appointments, name='appointments'),
    path('appointments/<int:pk>/', views.appointment_detail, name='appointment_detail'),
    path('patient-book-appointment/', views.patient_book_appointment_view, name='patient-book-appointment'),

    # Role Selection
    path('adminclick/', views.adminclick_view, name='adminclick'),
    path('doctorclick/', views.doctorclick_view, name='doctorclick'),
    path('patientclick/', views.patientclick_view, name='patientclick'),

    # Signup
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
    path('approve-doctor/<int:pk>/', views.approve_doctor_view, name='approve_doctor'),  
    path('reject-doctor/<int:pk>/', views.reject_doctor_view, name='reject_doctor'),
    path('edit-doctor/<int:pk>/', views.edit_doctor, name='edit_doctor'),
    path('delete-doctor/<int:pk>/', views.delete_doctor_view, name='delete_doctor'),
    path('admin-doctor/', views.admin_doctor_view, name='admin-doctor'),
    path('admin-approve-patient/', views.admin_approve_patient_view, name='admin-approve-patient'),
    path('admin-discharge-patient/', views.admin_discharge_patient_view, name='admin-discharge-patient'),
    # Admin - Patient Management
    path('admin-patient/', views.admin_patient_view, name='admin-patient'),
    path('admin-view-patient/', views.admin_view_patient_view, name='admin-view-patient'),
    path('admin-add-patient/', views.admin_add_patient_view, name='admin-add-patient'),
    path('edit-patient/<int:pk>/', views.edit_patient_view, name='edit-patient'),  # ✅ Fixed here
    path('delete_patient/<int:pk>/', views.delete_patient_view, name='delete_patient'),
    path('discharge_patient/<int:pk>/', views.discharge_patient_view, name='discharge_patient'),
    path('admin-appointment/', views.admin_appointment_view, name='admin-appointment'),
    path('admin-view-appointment/', views.admin_view_appointment, name='admin-view-appointment'),

    # Optional (Uncomment if you implement these views)
    
    # path('admin-view-appointment/', views.admin_view_appointment_view, name='admin-view-appointment'),
    # path('approve-appointment/<int:pk>/', views.approve_appointment_view, name='approve-appointment'),
    # path('reject-appointment/<int:pk>/', views.reject_appointment_view, name='reject-appointment'),
    # path('download-bill/<int:pk>/', views.download_pdf_view, name='download-bill'),
]
