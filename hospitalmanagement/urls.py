from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from hospital import views

urlpatterns = [
    # ---------- 🔹 Admin site ----------
    path('admin/', admin.site.urls),

    # ---------- 🔹 Homepage ----------
    path('', views.home_view, name='home'),

    # ---------- 🔹 Appointment Routes ----------
    path('appointments/', views.list_appointments, name='appointments'),
    path('appointments/<int:pk>/', views.appointment_detail, name='appointment_detail'),

    # ---------- 🔹 Static Info Pages ----------
    path('aboutus/', views.aboutus_view, name='aboutus'),
    path('contactus/', views.contactus_view, name='contactus'),

    # ---------- 🔹 Role Selection ----------
    path('adminclick/', views.adminclick_view, name='adminclick'),
    path('doctorclick/', views.doctorclick_view, name='doctorclick'),
    path('patientclick/', views.patientclick_view, name='patientclick'),

    # ---------- 🔹 Sign Up Routes ----------
    path('adminsignup/', views.admin_signup_view, name='adminsignup'),
    path('doctorsignup/', views.doctor_signup_view, name='doctorsignup'),
    path('patientsignup/', views.patient_signup_view, name='patientsignup'),

    # ---------- 🔹 Auth ----------
    path('adminlogin/', LoginView.as_view(template_name='hospital/adminlogin.html'), name='adminlogin'),
    path('doctorlogin/', LoginView.as_view(template_name='hospital/doctorlogin.html'), name='doctorlogin'),
    path('patientlogin/', LoginView.as_view(template_name='hospital/patientlogin.html'), name='patientlogin'),
    path('afterlogin/', views.afterlogin_view, name='afterlogin'),
    path('logout/', LogoutView.as_view(template_name='hospital/index.html'), name='logout'),

    # ---------- 🔹 Admin Views ----------
    # (unchanged from your version — trimmed here for brevity)
    path('admin-dashboard/', views.admin_dashboard_view, name='admin-dashboard'),
    path('admin-doctor/', views.admin_doctor_view, name='admin-doctor'),
    # ... (continue all your other admin paths as-is)

    # ---------- 🔹 Doctor Views ----------
    path('doctor-dashboard/', views.doctor_dashboard_view, name='doctor-dashboard'),
    # ... (keep existing doctor routes)

    # ---------- 🔹 Patient Views ----------
    path('patient-dashboard/', views.patient_dashboard_view, name='patient-dashboard'),
    path('patient-appointment/', views.patient_appointment_view, name='patient-appointment'),
    path('patient-book-appointment/', views.patient_book_appointment_view, name='patient-book-appointment'),
    path('patient-view-appointment/', views.patient_view_appointment_view, name='patient-view-appointment'),
    path('patient-view-doctor/', views.patient_view_doctor_view, name='patient-view-doctor'),
    path('searchdoctor/', views.search_doctor_view, name='searchdoctor'),
    path('patient-discharge/', views.patient_discharge_view, name='patient-discharge'),
]
