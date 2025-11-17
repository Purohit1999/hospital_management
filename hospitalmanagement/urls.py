from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView
from hospital import views

urlpatterns = [
    # Admin site
    path('admin/', admin.site.urls),

    # Static pages
    path('', views.home_view, name='home'),
    path('aboutus/', views.aboutus_view, name='aboutus'),
    path('contactus/', views.contactus_view, name='contactus'),
    path('contact-success/', views.contact_success_view, name='contact-success'),

    # Role-based click views
    path('adminclick/', views.adminclick_view, name='adminclick'),
    path('doctorclick/', views.doctorclick_view, name='doctorclick'),
    path('patientclick/', views.patientclick_view, name='patientclick'),

    # Signup routes
    path('adminsignup/', views.admin_signup_view, name='adminsignup'),
    path('doctorsignup/', views.doctor_signup_view, name='doctorsignup'),
    path('patientsignup/', views.patient_signup_view, name='patientsignup'),

    # Login routes
    path('adminlogin/', views.adminlogin_view, name='adminlogin'),
    path('doctorlogin/', views.doctor_login_view, name='doctorlogin'),
    path(
        'patientlogin/',
        LoginView.as_view(template_name='hospital/patientlogin.html'),
        name='patientlogin'
    ),

    # After login
    path('afterlogin/', views.afterlogin_view, name='afterlogin'),

    # Logout
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),

    # Dashboards
    path('admin-dashboard/', views.admin_dashboard_view, name='admin-dashboard'),
    path('doctor-dashboard/', views.doctor_dashboard_view, name='doctor-dashboard'),
    path('patient-dashboard/', views.patient_dashboard_view, name='patient-dashboard'),

    # Doctor Panel Views
    path('doctor-view-patient/', views.doctor_view_patient_view, name='doctor-view-patient'),
    path('doctor-view-appointment/', views.doctor_view_appointment_view, name='doctor-view-appointment'),
    path('doctor-search-patient/', views.doctor_search_patient_view, name='doctor-search-patient'),
    path('doctor-view-discharge-patient/', views.doctor_view_discharge_patient_view,
         name='doctor-view-discharge-patient'),

    # Admin - Doctor Management
    path('admin-doctor/', views.admin_doctor_view, name='admin-doctor'),
    path('admin-view-doctor/', views.admin_view_doctor_view, name='admin-view-doctor'),
    path('admin-add-doctor/', views.admin_add_doctor_view, name='admin-add-doctor'),
    path('admin-approve-doctor/', views.admin_approve_doctor_view, name='admin-approve-doctor'),
    path('admin-view-doctor-specialisation/', views.admin_view_doctor_specialisation,
         name='admin-view-doctor-specialisation'),

    path('approve-doctor/<int:pk>/', views.approve_doctor_view, name='approve-doctor'),
    path('reject-doctor/<int:pk>/', views.reject_doctor_view, name='reject-doctor'),
    path('edit-doctor/<int:pk>/', views.edit_doctor_view, name='edit-doctor'),
    path('delete-doctor/<int:pk>/', views.delete_doctor_view, name='delete-doctor-from-hospital'),

    # Admin - Patient Management
    path('admin-patient/', views.admin_patient_view, name='admin-patient'),
    path('admin-view-patient/', views.admin_view_patient_view, name='admin-view-patient'),
    path('admin-add-patient/', views.admin_add_patient_view, name='admin-add-patient'),
    path('admin-approve-patient/', views.admin_approve_patient_view, name='admin-approve-patient'),

    path('approve-patient/<int:pk>/', views.approve_patient_view, name='approve-patient'),
    path('reject-patient/<int:pk>/', views.reject_patient_view, name='reject-patient'),
    path('edit-patient/<int:pk>/', views.edit_patient_view, name='edit-patient'),
    path('delete-patient/<int:pk>/', views.delete_patient_view, name='delete-patient'),

    # Patient discharge & billing
    path('patient/discharge-summary/', views.patient_discharge_summary_view,
         name='patient-discharge-summary'),
    path('discharge-patient/<int:pk>/', views.discharge_patient_view, name='discharge-patient'),
    path('generate-bill/<int:pk>/', views.generate_patient_bill_view, name='generate-bill'),

    # Admin - Appointment Management
    path('admin-appointment/', views.admin_appointment_view, name='admin-appointment'),
    path('admin-view-appointment/', views.admin_view_appointment, name='admin-view-appointment'),
    path('admin-add-appointment/', views.admin_add_appointment_view, name='admin-add-appointment'),
    path('admin-approve-appointment/', views.admin_approve_appointment_view,
         name='admin-approve-appointment'),
    path('admin-discharge-patient/', views.admin_discharge_patient_view,
         name='admin-discharge-patient'),

    # Public/Patient Appointment Views
    path('appointments/', views.list_appointments, name='appointments'),
    path('appointments/<int:pk>/', views.appointment_detail, name='appointment_detail'),
    path('patient-book-appointment/', views.patient_book_appointment_view,
         name='patient-book-appointment'),
    path('patient-appointments/', views.patient_appointment_list_view,
         name='patient-appointment-list'),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
