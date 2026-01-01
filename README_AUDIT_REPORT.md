# README Audit Report

Repository: C:\Users\puroh\Documents\hospital_management
GitHub: https://github.com/Purohit1999/hospital_management
Live site: https://hospital-management-web-4963f51d811d.herokuapp.com

## Summary Table

| Claim | Repo Evidence | Live Evidence (public only) | Status | Notes |
| ----- | ------------- | --------------------------- | ------ | ----- |
| --- | No local match found | - | FAIL | # 🏥 **Hospital Management System — Full Stack Django Application** |
| --- | No local match found | - | FAIL | # 📖 **Table of Contents** |
| --- | No local match found | - | FAIL | # 📌 **Project Overview** |
| --- | No local match found | - | FAIL | # 👤 **User Stories** |
| --- | No local match found | - | FAIL | # 🧑‍⚕️ **Admin User Stories** |
| **I should be able to:** | hospitalmanagement\settings.py: # Use environment variable to control DEBUG | hospitalmanagement\settings.py: STRIPE_PUBLISHABLE_KEY = os.environ.get("STRIPE_PUBLISHABLE_KEY", "") | hospitalmanagement\settings.py: AI_FEATURES_ENABLED = _truthy(os.getenv("AI_FEATURES_ENABLED", "True")) | - | PARTIAL | ### 🟢 **1. Register or Approve Doctors & Patients** |
| * View all pending registration requests | hospitalmanagement\settings.py: "django.middleware.csrf.CsrfViewMiddleware", | hospitalmanagement\urls.py: from django.contrib.auth.views import LogoutView | hospitalmanagement\urls.py: from hospital import views, views_stripe_test | - | PARTIAL | ### 🟢 **1. Register or Approve Doctors & Patients** |
| * Approve, reject, or delete accounts | hospitalmanagement\urls.py: path('admin-approve-doctor/', views.admin_approve_doctor_view, name='admin-approve-doctor'), | hospitalmanagement\urls.py: path('approve-doctor/<int:pk>/', views.approve_doctor_view, name='approve-doctor'), | hospitalmanagement\urls.py: path('reject-doctor/<int:pk>/', views.reject_doctor_view, name='reject-doctor'), | - | PARTIAL | ### 🟢 **1. Register or Approve Doctors & Patients** |
| * Ensure secure access to sensitive data | hospitalmanagement\settings.py: SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https") | hospitalmanagement\settings.py: SECURE_CROSS_ORIGIN_OPENER_POLICY = "same-origin" | hospital\views.py: "Access denied: You are not an admin user.", | - | PARTIAL | ### 🟢 **1. Register or Approve Doctors & Patients** |
| * See account status updates instantly | hospital\views.py: doctor.status = False | hospital\views.py: error_message = "Access denied: Please log in using a patient account." | hospital\views.py: doctors = Doctor.objects.filter(status=False).select_related("user") | - | PARTIAL | ### 🟢 **1. Register or Approve Doctors & Patients** |
| --- | No local match found | - | FAIL | ### 🟢 **1. Register or Approve Doctors & Patients** |
| **This includes:** | No local match found | - | FAIL | ### 📝 **2. Add & Manage Appointments** |
| * Creating new appointments | hospitalmanagement\urls.py: path('appointments/', views.list_appointments, name='appointments'), | hospitalmanagement\urls.py: path('appointments/<int:pk>/', views.appointment_detail, name='appointment_detail'), | hospitalmanagement\urls.py: 'patient-appointments/', | - | PARTIAL | ### 📝 **2. Add & Manage Appointments** |
| * Approving or denying appointment requests | hospitalmanagement\urls.py: path('doctor-view-appointment/', views.doctor_view_appointment_view, name='doctor-view-appointment'), | hospitalmanagement\urls.py: 'admin-consultation-requests/', | hospitalmanagement\urls.py: views.admin_consultation_requests_view, | - | PARTIAL | ### 📝 **2. Add & Manage Appointments** |
| * Rescheduling or cancelling bookings | No local match found | - | FAIL | ### 📝 **2. Add & Manage Appointments** |
| * Viewing all appointments in date order | hospitalmanagement\urls.py: path('admin-update-doctor/<int:pk>/', views.edit_doctor_view, name='admin-update-doctor'), | hospitalmanagement\urls.py: path('admin-update-patient/<int:pk>/', views.edit_patient_view, name='admin-update-patient'), | hospitalmanagement\urls.py: path('admin-update-appointment/<int:pk>/', views.admin_update_appointment_view, name='admin-update-appointment'), | - | PARTIAL | ### 📝 **2. Add & Manage Appointments** |
| --- | No local match found | - | FAIL | ### 📝 **2. Add & Manage Appointments** |
| **I should be able to:** | hospitalmanagement\settings.py: # Use environment variable to control DEBUG | hospitalmanagement\settings.py: STRIPE_PUBLISHABLE_KEY = os.environ.get("STRIPE_PUBLISHABLE_KEY", "") | hospitalmanagement\settings.py: AI_FEATURES_ENABLED = _truthy(os.getenv("AI_FEATURES_ENABLED", "True")) | - | PARTIAL | ### 🔍 **3. View & Update Doctor/Patient Records** |
| * Search for users | hospitalmanagement\urls.py: path('doctor-search-patient/', views.doctor_search_patient_view, name='doctor-search-patient'), | hospital\views.py: demo_users = ( | hospital\views.py: {"demo_users": demo_users}, | - | PARTIAL | ### 🔍 **3. View & Update Doctor/Patient Records** |
| * Edit or delete records | hospitalmanagement\urls.py: path('edit-doctor/<int:pk>/', views.edit_doctor_view, name='edit-doctor'), | hospitalmanagement\urls.py: path('delete-doctor/<int:pk>/', views.delete_doctor_view, name='delete-doctor'), | hospitalmanagement\urls.py: path('admin-update-doctor/<int:pk>/', views.edit_doctor_view, name='admin-update-doctor'), | - | PARTIAL | ### 🔍 **3. View & Update Doctor/Patient Records** |
| * Update profile information | hospitalmanagement\settings.py: # Default storage for uploaded files (profile pictures, etc.) | hospitalmanagement\urls.py: path('admin-update-doctor/<int:pk>/', views.edit_doctor_view, name='admin-update-doctor'), | hospitalmanagement\urls.py: path('admin-update-patient/<int:pk>/', views.edit_patient_view, name='admin-update-patient'), | - | PARTIAL | ### 🔍 **3. View & Update Doctor/Patient Records** |
| * View medical or administrative details | hospitalmanagement\settings.py: "django.middleware.csrf.CsrfViewMiddleware", | hospitalmanagement\urls.py: from django.contrib.auth.views import LogoutView | hospitalmanagement\urls.py: from hospital import views, views_stripe_test | - | PARTIAL | ### 🔍 **3. View & Update Doctor/Patient Records** |
| --- | No local match found | - | FAIL | ### 🔍 **3. View & Update Doctor/Patient Records** |
| **I can:** | No local match found | - | FAIL | ### 🧾 **4. Generate Bills & Discharge Summaries** |
| * Generate final invoices | hospitalmanagement\urls.py: path('generate-bill/<int:pk>/', views.generate_patient_bill_view, name='generate-bill'), | hospital\views.py: invoices = Invoice.objects.filter(patient=patient).order_by("-id") | hospital\views.py: "invoices": invoices, | - | PARTIAL | ### 🧾 **4. Generate Bills & Discharge Summaries** |
| * Add doctor fees, room charges, medicine fees | hospitalmanagement\urls.py: path('doctorclick/', views.doctorclick_view, name='doctorclick'), | hospitalmanagement\urls.py: path('doctorsignup/', views.doctor_signup_view, name='doctorsignup'), | hospitalmanagement\urls.py: path('doctorlogin/', views.doctor_login_view, name='doctorlogin'), | - | PARTIAL | ### 🧾 **4. Generate Bills & Discharge Summaries** |
| * Download discharge summaries | hospitalmanagement\urls.py: 'doctor-view-discharge-patient/', | hospitalmanagement\urls.py: views.doctor_view_discharge_patient_view, | hospitalmanagement\urls.py: name='doctor-view-discharge-patient' | - | PARTIAL | ### 🧾 **4. Generate Bills & Discharge Summaries** |
| * Store records for future reference | templates\hospital\aboutus.html: This platform assists with scheduling appointments, managing patient records, | templates\hospital\admin_doctor.html: <!-- View Doctor Records --> | templates\hospital\admin_view_doctor.html: <h4 class="section-title">Doctor Records</h4> | - | PARTIAL | ### 🧾 **4. Generate Bills & Discharge Summaries** |
| --- | No local match found | - | FAIL | ### 🧾 **4. Generate Bills & Discharge Summaries** |
| **Dashboard shows:** | hospitalmanagement\urls.py: # Dashboards | hospitalmanagement\urls.py: path('admin-dashboard/', views.admin_dashboard_view, name='admin-dashboard'), | hospitalmanagement\urls.py: path('doctor-dashboard/', views.doctor_dashboard_view, name='doctor-dashboard'), | - | PARTIAL | ### 📊 **5. Access the Admin Dashboard** |
| * Pending approvals | hospital\views.py: context = {"pending_doctors": doctors} | hospital\views.py: "Failed to load pending doctors", | hospital\views.py: "pending_doctors": [], | - | PARTIAL | ### 📊 **5. Access the Admin Dashboard** |
| * Total appointments | hospitalmanagement\urls.py: path('appointments/', views.list_appointments, name='appointments'), | hospitalmanagement\urls.py: path('appointments/<int:pk>/', views.appointment_detail, name='appointment_detail'), | hospitalmanagement\urls.py: 'patient-appointments/', | - | PARTIAL | ### 📊 **5. Access the Admin Dashboard** |
| * Total patients and doctors | hospitalmanagement\urls.py: path('doctorsignup/', views.doctor_signup_view, name='doctorsignup'), | hospitalmanagement\urls.py: path('patientsignup/', views.patient_signup_view, name='patientsignup'), | hospital\views.py: "hospital/doctorsignup.html", | - | PARTIAL | ### 📊 **5. Access the Admin Dashboard** |
| * Latest system activity | hospitalmanagement\settings.py: "BACKEND": "django.core.files.storage.FileSystemStorage", | hospital\views.py: - Shows latest appointment's doctor & date (if any) | hospital\views.py: latest_appointment = ( | - | PARTIAL | ### 📊 **5. Access the Admin Dashboard** |
| --- | No local match found | - | FAIL | ### 📊 **5. Access the Admin Dashboard** |
| --- | No local match found | - | FAIL | ### 🔒 **6. Enforce Role-Based Authentication** |
| --- | No local match found | - | FAIL | # 🩺 **Doctor User Stories** |
| **I can:** | No local match found | - | FAIL | ### 📅 **1. View My Appointments** |
| * View appointments assigned to me | hospitalmanagement\settings.py: "django.middleware.csrf.CsrfViewMiddleware", | hospitalmanagement\urls.py: from django.contrib.auth.views import LogoutView | hospitalmanagement\urls.py: from hospital import views, views_stripe_test | - | PARTIAL | ### 📅 **1. View My Appointments** |
| * Sort by date and time | hospitalmanagement\settings.py: TIME_ZONE = "Europe/London" | hospitalmanagement\settings.py: "format": "%(levelname)s %(asctime)s %(name)s %(message)s", | hospitalmanagement\urls.py: path('admin-update-doctor/<int:pk>/', views.edit_doctor_view, name='admin-update-doctor'), | - | PARTIAL | ### 📅 **1. View My Appointments** |
| * Check patient names, symptoms, and notes | hospitalmanagement\urls.py: path('patientclick/', views.patientclick_view, name='patientclick'), | hospitalmanagement\urls.py: path('patientsignup/', views.patient_signup_view, name='patientsignup'), | hospitalmanagement\urls.py: 'patientlogin/', | - | PARTIAL | ### 📅 **1. View My Appointments** |
| --- | No local match found | - | FAIL | ### 📅 **1. View My Appointments** |
| **I can:** | No local match found | - | FAIL | ### 👨‍⚕️ **2. Access Assigned Patients** |
| * View patient details and medical history | hospitalmanagement\settings.py: "django.middleware.csrf.CsrfViewMiddleware", | hospitalmanagement\urls.py: from django.contrib.auth.views import LogoutView | hospitalmanagement\urls.py: from hospital import views, views_stripe_test | - | PARTIAL | ### 👨‍⚕️ **2. Access Assigned Patients** |
| * Access submitted symptoms and prior treatments | hospital\views.py: "A new consultation request has been submitted.\n\n" | hospital\views.py: "Access denied: You are not an admin user.", | hospital\views.py: "Access denied: Your doctor profile is missing or not approved." | - | PARTIAL | ### 👨‍⚕️ **2. Access Assigned Patients** |
| * See profile images for easy identification | hospitalmanagement\settings.py: # Default storage for uploaded files (profile pictures, etc.) | hospital\views.py: "Patient profile not found. Please complete registration.", | hospital\views.py: "Access denied: Your doctor profile is missing or not approved." | - | PARTIAL | ### 👨‍⚕️ **2. Access Assigned Patients** |
| --- | No local match found | - | FAIL | ### 👨‍⚕️ **2. Access Assigned Patients** |
| **I can:** | No local match found | - | FAIL | ### 💊 **3. Issue Prescriptions** |
| * Add medication names | hospital\models.py: medications = models.TextField() | ai_hub\views.py: "step_names": [step.get("step") for step in trace], | ai_hub\views.py: "feature_names": list(features.keys()), | - | PARTIAL | ### 💊 **3. Issue Prescriptions** |
| * Add dosage & timings | No local match found | - | FAIL | ### 💊 **3. Issue Prescriptions** |
| * Create downloadable notes for patients | hospitalmanagement\urls.py: path('patientsignup/', views.patient_signup_view, name='patientsignup'), | hospitalmanagement\urls.py: "patient/create-checkout-session/<int:discharge_id>/", | hospitalmanagement\urls.py: payment_views.create_checkout_session, | - | PARTIAL | ### 💊 **3. Issue Prescriptions** |
| --- | No local match found | - | FAIL | ### 💊 **3. Issue Prescriptions** |
| --- | No local match found | - | FAIL | ### 🗂 **4. View Past Discharge Summaries** |
| --- | No local match found | - | FAIL | ### 🛡 **5. Access Only My Patients** |
| --- | No local match found | - | FAIL | # 🧑‍🦽 **Patient User Stories** |
| **I provide:** | hospitalmanagement\settings.py: LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai").strip().lower() | hospitalmanagement\settings.py: RAG_PROVIDER = os.getenv("RAG_PROVIDER", "faiss") | ai_hub\views.py: "Use the provided context to answer the question. " | - | PARTIAL | ### 🧾 **1. Register Easily** |
| * Basic personal details | hospital\views.py: from .models import Doctor, Patient, Appointment, DischargeDetails, Invoice, EmailLog | hospital\views.py: Uses DischargeDetails.doctor foreign key. | hospital\views.py: discharged_patients = DischargeDetails.objects.filter( | - | PARTIAL | ### 🧾 **1. Register Easily** |
| * Contact information | hospitalmanagement\urls.py: path('contactus/', views.contactus_view, name='contactus'), | hospitalmanagement\urls.py: path('contact-success/', views.contact_success_view, name='contact-success'), | hospital\views.py: ContactForm,          # 👈 contact form import | - | PARTIAL | ### 🧾 **1. Register Easily** |
| * Symptoms | hospital\views.py: | Q(symptoms__icontains=query) | hospital\views.py: "symptoms": patient.symptoms, | hospital\views.py: f"Discharged due to recovery from symptoms: {patient.symptoms}" | - | PARTIAL | ### 🧾 **1. Register Easily** |
| * Optional profile photo | hospitalmanagement\settings.py: # Default storage for uploaded files (profile pictures, etc.) | hospital\views.py: "Patient profile not found. Please complete registration.", | hospital\views.py: # Optional user feedback | - | PARTIAL | ### 🧾 **1. Register Easily** |
| --- | No local match found | - | FAIL | ### 🧾 **1. Register Easily** |
| **I can:** | No local match found | - | FAIL | ### 📅 **2. Book Appointments** |
| * Choose a doctor | hospitalmanagement\urls.py: path('doctorclick/', views.doctorclick_view, name='doctorclick'), | hospitalmanagement\urls.py: path('doctorsignup/', views.doctor_signup_view, name='doctorsignup'), | hospitalmanagement\urls.py: path('doctorlogin/', views.doctor_login_view, name='doctorlogin'), | - | PARTIAL | ### 📅 **2. Book Appointments** |
| * Select appointment date | hospitalmanagement\urls.py: path('doctor-view-appointment/', views.doctor_view_appointment_view, name='doctor-view-appointment'), | hospitalmanagement\urls.py: path('admin-update-doctor/<int:pk>/', views.edit_doctor_view, name='admin-update-doctor'), | hospitalmanagement\urls.py: path('admin-update-patient/<int:pk>/', views.edit_patient_view, name='admin-update-patient'), | - | PARTIAL | ### 📅 **2. Book Appointments** |
| * Get confirmation instantly | No local match found | - | FAIL | ### 📅 **2. Book Appointments** |
| --- | No local match found | - | FAIL | ### 📅 **2. Book Appointments** |
| --- | No local match found | - | FAIL | ### 🔎 **3. View Appointment History** |
| --- | No local match found | - | FAIL | ### 📄 **4. View Billing & Discharge Information** |
| --- | No local match found | - | FAIL | ### 💬 **5. Send Feedback / Contact Form** |
| --- | No local match found | - | FAIL | ### UX Goals |
| --- | No local match found | - | FAIL | ### 📲 Mobile |
| * HTML5 | No local match found | - | FAIL | ### **Frontend** |
| * CSS3 / Bootstrap | templates\hospital\adminlogin.html: <!-- Bootstrap & Font Awesome --> | templates\hospital\adminlogin.html: <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet"> | templates\hospital\adminsignup.html: <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet"> | - | PARTIAL | ### **Frontend** |
| * JavaScript | No local match found | - | FAIL | ### **Frontend** |
| * Django | hospitalmanagement\settings.py: "django.contrib.admin", | hospitalmanagement\settings.py: "django.contrib.auth", | hospitalmanagement\settings.py: "django.contrib.contenttypes", | - | PARTIAL | ### **Backend** |
| * Python | No local match found | - | FAIL | ### **Backend** |
| * Django ModelForms | hospitalmanagement\settings.py: "django.contrib.admin", | hospitalmanagement\settings.py: "django.contrib.auth", | hospitalmanagement\settings.py: "django.contrib.contenttypes", | - | PARTIAL | ### **Backend** |
| * Django ORM | hospitalmanagement\settings.py: "django.contrib.admin", | hospitalmanagement\settings.py: "django.contrib.auth", | hospitalmanagement\settings.py: "django.contrib.contenttypes", | - | PARTIAL | ### **Backend** |
| * SQLite (Local) | hospitalmanagement\settings.py: # Default = True for local dev. On Heroku set DEBUG=false in Config Vars. | hospitalmanagement\settings.py: # ✔ ALLOWED_HOSTS — LOCAL + HEROKU APPS | hospitalmanagement\settings.py: for host in os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",") | - | PARTIAL | ### **Database** |
| * PostgreSQL (Heroku) | hospitalmanagement\settings.py: # Default = True for local dev. On Heroku set DEBUG=false in Config Vars. | hospitalmanagement\settings.py: # ✔ ALLOWED_HOSTS — LOCAL + HEROKU APPS | hospitalmanagement\settings.py: # ✔ Needed for Heroku reverse proxy | - | PARTIAL | ### **Database** |
| * Heroku | hospitalmanagement\settings.py: # Default = True for local dev. On Heroku set DEBUG=false in Config Vars. | hospitalmanagement\settings.py: # ✔ ALLOWED_HOSTS — LOCAL + HEROKU APPS | hospitalmanagement\settings.py: # ✔ Needed for Heroku reverse proxy | - | PARTIAL | ### **Deployment** |
| * GitHub | No local match found | - | FAIL | ### **Deployment** |
| * WhiteNoise | hospitalmanagement\settings.py: "whitenoise.middleware.WhiteNoiseMiddleware",  # static files on Heroku | hospitalmanagement\settings.py: STATICFILES_BACKEND = "whitenoise.storage.CompressedManifestStaticFilesStorage" | hospitalmanagement\settings.py: # Storage for static files (served via WhiteNoise on Heroku) | - | PARTIAL | ### **Deployment** |
| * Gunicorn | No local match found | - | FAIL | ### **Deployment** |
| --- | No local match found | - | FAIL | ### **Deployment** |
| --- | No local match found | - | FAIL | # 📂 **System Architecture** |
| * One-to-One: User ↔ Doctor, User ↔ Patient | hospitalmanagement\settings.py: {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"}, | hospitalmanagement\settings.py: EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", "") | hospitalmanagement\settings.py: EMAIL_HOST_USER or "no-reply@example.com", | - | PARTIAL | # 🗄 **Data Models** |
| * Many-to-One: Patient → Appointments | hospitalmanagement\urls.py: path('patientclick/', views.patientclick_view, name='patientclick'), | hospitalmanagement\urls.py: path('patientsignup/', views.patient_signup_view, name='patientsignup'), | hospitalmanagement\urls.py: 'patientlogin/', | - | PARTIAL | # 🗄 **Data Models** |
| * One-to-Many: Patient → Discharge Summaries | hospitalmanagement\urls.py: path('patientclick/', views.patientclick_view, name='patientclick'), | hospitalmanagement\urls.py: path('patientsignup/', views.patient_signup_view, name='patientsignup'), | hospitalmanagement\urls.py: 'patientlogin/', | - | PARTIAL | # 🗄 **Data Models** |
| - user_id (OneToOne -> auth_user) | hospital\views.py: logger.info("Auto-login after signup", extra={"user_id": user.id}) | hospital\models.py: user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True) | hospital\models.py: user = models.OneToOneField(User, on_delete=models.CASCADE) | - | PARTIAL | ## Full Data Schema (Tables + Fields) |
| - department, mobile, address, profile_pic, status, created_at | hospital\views.py: "mobile": patient.mobile, | hospital\views.py: "address": patient.address, | hospital\views.py: "mobile": patient.mobile, | - | PARTIAL | ## Full Data Schema (Tables + Fields) |
| - user_id (OneToOne -> auth_user) | hospital\views.py: logger.info("Auto-login after signup", extra={"user_id": user.id}) | hospital\models.py: user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True) | hospital\models.py: user = models.OneToOneField(User, on_delete=models.CASCADE) | - | PARTIAL | ## Full Data Schema (Tables + Fields) |
| - address, mobile, symptoms, profile_pic, assignedDoctorId (FK -> Doctor), status, created_at | hospital\views.py: | Q(symptoms__icontains=query) | hospital\views.py: "mobile": patient.mobile, | hospital\views.py: "address": patient.address, | - | PARTIAL | ## Full Data Schema (Tables + Fields) |
| - patient_id (FK -> Patient) | hospitalmanagement\urls.py: path('patientclick/', views.patientclick_view, name='patientclick'), | hospitalmanagement\urls.py: path('patientsignup/', views.patient_signup_view, name='patientsignup'), | hospitalmanagement\urls.py: 'patientlogin/', | - | PARTIAL | ## Full Data Schema (Tables + Fields) |
| - doctor_id (FK -> Doctor) | hospitalmanagement\urls.py: path('doctorclick/', views.doctorclick_view, name='doctorclick'), | hospitalmanagement\urls.py: path('doctorsignup/', views.doctor_signup_view, name='doctorsignup'), | hospitalmanagement\urls.py: path('doctorlogin/', views.doctor_login_view, name='doctorlogin'), | - | PARTIAL | ## Full Data Schema (Tables + Fields) |
| - date_time, description, status, created_at | hospital\views.py: doctor.status = False | hospital\views.py: doctors = Doctor.objects.filter(status=False).select_related("user") | hospital\views.py: .order_by("-date_time") | - | PARTIAL | ## Full Data Schema (Tables + Fields) |
| - created_by_id, updated_by_id (FK -> auth_user) | payments\models.py: settings.AUTH_USER_MODEL, | ai_hub\models.py: settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True | ai_hub\models.py: settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True | - | PARTIAL | ## Full Data Schema (Tables + Fields) |
| - patient_id (FK -> Patient) | hospitalmanagement\urls.py: path('patientclick/', views.patientclick_view, name='patientclick'), | hospitalmanagement\urls.py: path('patientsignup/', views.patient_signup_view, name='patientsignup'), | hospitalmanagement\urls.py: 'patientlogin/', | - | PARTIAL | ## Full Data Schema (Tables + Fields) |
| - doctor_id (FK -> Doctor, nullable) | hospitalmanagement\urls.py: path('doctorclick/', views.doctorclick_view, name='doctorclick'), | hospitalmanagement\urls.py: path('doctorsignup/', views.doctor_signup_view, name='doctorsignup'), | hospitalmanagement\urls.py: path('doctorlogin/', views.doctor_login_view, name='doctorlogin'), | - | PARTIAL | ## Full Data Schema (Tables + Fields) |
| - admission_date, discharge_date, summary | hospitalmanagement\urls.py: 'patient/discharge-summary/', | hospitalmanagement\urls.py: views.patient_discharge_summary_view, | hospitalmanagement\urls.py: name='patient-discharge-summary' | - | PARTIAL | ## Full Data Schema (Tables + Fields) |
| - room_charge, doctor_fee, medicine_cost, other_charge, total, created_at | hospital\views.py: room_charge = safe_float(request.POST.get("roomCharge", 0)) * total_days | hospital\views.py: doctor_fee = safe_float(request.POST.get("doctorFee", 0)) | hospital\views.py: medicine_cost = safe_float(request.POST.get("medicineCost", 0)) | - | PARTIAL | ## Full Data Schema (Tables + Fields) |
| - patient_id (FK -> Patient) | hospitalmanagement\urls.py: path('patientclick/', views.patientclick_view, name='patientclick'), | hospitalmanagement\urls.py: path('patientsignup/', views.patient_signup_view, name='patientsignup'), | hospitalmanagement\urls.py: 'patientlogin/', | - | PARTIAL | ## Full Data Schema (Tables + Fields) |
| - issued_date, amount, paid, created_at, created_by_id (FK -> auth_user) | hospital\views.py: payments_count = Payment.objects.filter(patient=patient, status="paid").count() | hospital\views.py: requests = ConsultationRequest.objects.order_by("-created_at") | hospital\views.py: if discharge.payment and discharge.payment.status == "paid": | - | PARTIAL | ## Full Data Schema (Tables + Fields) |
| - user_id (FK -> auth_user) | hospital\views.py: logger.info("Auto-login after signup", extra={"user_id": user.id}) | payments\models.py: settings.AUTH_USER_MODEL, | ai_hub\models.py: settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True | - | PARTIAL | ## Full Data Schema (Tables + Fields) |
| - patient_id (FK -> Patient) | hospitalmanagement\urls.py: path('patientclick/', views.patientclick_view, name='patientclick'), | hospitalmanagement\urls.py: path('patientsignup/', views.patient_signup_view, name='patientsignup'), | hospitalmanagement\urls.py: 'patientlogin/', | - | PARTIAL | ## Full Data Schema (Tables + Fields) |
| - discharge_id (FK -> DischargeDetails, nullable) | hospitalmanagement\urls.py: "patient/create-checkout-session/<int:discharge_id>/", | hospital\views.py: from .models import Doctor, Patient, Appointment, DischargeDetails, Invoice, EmailLog | hospital\views.py: Uses DischargeDetails.doctor foreign key. | - | PARTIAL | ## Full Data Schema (Tables + Fields) |
| - amount, currency, stripe_session_id, stripe_payment_intent, status, created_at | hospitalmanagement\settings.py: STRIPE_CURRENCY = "gbp" | hospital\models.py: stripe_session_id = models.CharField(max_length=255, blank=True, null=True) | hospital\models.py: amount = models.DecimalField(max_digits=8, decimal_places=2) | - | PARTIAL | ## Full Data Schema (Tables + Fields) |
| - appointment_id (OneToOne -> Appointment) | hospitalmanagement\urls.py: path('doctor-view-appointment/', views.doctor_view_appointment_view, name='doctor-view-appointment'), | hospitalmanagement\urls.py: # Admin - Appointment Management | hospitalmanagement\urls.py: path('admin-appointment/', views.admin_appointment_view, name='admin-appointment'), | - | PARTIAL | ## Full Data Schema (Tables + Fields) |
| - date_issued, medications, instructions, created_at, created_by_id (FK -> auth_user) | hospital\views.py: requests = ConsultationRequest.objects.order_by("-created_at") | hospital\views.py: if patient and patient.created_at: | hospital\views.py: return patient.created_at.date() | - | PARTIAL | ## Full Data Schema (Tables + Fields) |
| - appointment_id (FK -> Appointment) | hospitalmanagement\urls.py: path('doctor-view-appointment/', views.doctor_view_appointment_view, name='doctor-view-appointment'), | hospitalmanagement\urls.py: # Admin - Appointment Management | hospitalmanagement\urls.py: path('admin-appointment/', views.admin_appointment_view, name='admin-appointment'), | - | PARTIAL | ## Full Data Schema (Tables + Fields) |
| - rating, comments, submitted_at | hospital\models.py: rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)]) | hospital\models.py: comments = models.TextField(blank=True) | hospital\models.py: submitted_at = models.DateTimeField(auto_now_add=True) | - | PARTIAL | ## Full Data Schema (Tables + Fields) |
| --- | No local match found | - | FAIL | ## Text ERD (Relationships) |
| --- | No local match found | - | FAIL | # 🔐 **Authentication & Authorization** |
| * Approve users | hospitalmanagement\urls.py: path('admin-approve-doctor/', views.admin_approve_doctor_view, name='admin-approve-doctor'), | hospitalmanagement\urls.py: path('approve-doctor/<int:pk>/', views.approve_doctor_view, name='approve-doctor'), | hospitalmanagement\urls.py: path('admin-approve-patient/', views.admin_approve_patient_view, name='admin-approve-patient'), | - | PARTIAL | ### **Admin** |
| * Manage appointments | hospitalmanagement\settings.py: ROOT_URLCONF = "hospitalmanagement.urls" | hospitalmanagement\settings.py: WSGI_APPLICATION = "hospitalmanagement.wsgi.application" | hospitalmanagement\urls.py: # Admin - Doctor Management | - | PARTIAL | ### **Admin** |
| * Billing + discharge | hospitalmanagement\urls.py: 'doctor-view-discharge-patient/', | hospitalmanagement\urls.py: views.doctor_view_discharge_patient_view, | hospitalmanagement\urls.py: name='doctor-view-discharge-patient' | - | PARTIAL | ### **Admin** |
| * View appointments | hospitalmanagement\settings.py: "django.middleware.csrf.CsrfViewMiddleware", | hospitalmanagement\urls.py: from django.contrib.auth.views import LogoutView | hospitalmanagement\urls.py: from hospital import views, views_stripe_test | - | PARTIAL | ### **Doctor** |
| * Patient access | hospitalmanagement\urls.py: path('patientclick/', views.patientclick_view, name='patientclick'), | hospitalmanagement\urls.py: path('patientsignup/', views.patient_signup_view, name='patientsignup'), | hospitalmanagement\urls.py: 'patientlogin/', | - | PARTIAL | ### **Doctor** |
| * Add diagnosis | No local match found | - | FAIL | ### **Doctor** |
| * Book appointments | hospitalmanagement\urls.py: path('book-consultation/', views.book_consultation_view, name='book-consultation'), | hospitalmanagement\urls.py: path('appointments/', views.list_appointments, name='appointments'), | hospitalmanagement\urls.py: path('appointments/<int:pk>/', views.appointment_detail, name='appointment_detail'), | - | PARTIAL | ### **Patient** |
| * Track visit history | hospital\views.py: # total patients (you could also track pending separately if needed) | payments\views.py: def payment_history_view(request): | payments\views.py: return render(request, "payments/history.html", {"payments": payments}) | - | PARTIAL | ### **Patient** |
| * Download reports | hospitalmanagement\urls.py: path('download-pdf/<int:pk>/', views.download_invoice_pdf_view, name='download-pdf'), | hospital\views.py: html = render_to_string("hospital/download_bill.html", context) | hospital\views.py: def download_invoice_pdf_view(request, pk): | - | PARTIAL | ### **Patient** |
| --- | No local match found | - | FAIL | ### **Patient** |
| --- | No local match found | - | FAIL | ### 3. Entity Relationship Diagram (ERD) |
| --- | No local match found | - | FAIL | # 💳 **Stripe Payment Integration** |
| --- | No local match found | - | FAIL | # 🧪 **Validation, Testing & Lighthouse** |
| --- | No local match found | - | FAIL | ## ✅ **Validation Summary Table** |
| --- | No local match found | - | FAIL | ### 🐍 Python (PEP8) Validation |
| --- | No local match found | - | FAIL | ## 📱 **Responsiveness Testing** |
| --- | No local match found | - | FAIL | ## 🌐 **Browser Compatibility Testing** |
| --- | No local match found | - | FAIL | ## 🧪 **Manual Testing Matrix** |
| --- | No local match found | - | FAIL | ### Screenshots |
| --- | No local match found | - | FAIL | # 🐞 Debugging & Issue Resolution |
| **Tool:** W3C HTML Validator (https://validator.w3.org/) | hospitalmanagement\settings.py: SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https") | hospitalmanagement\settings.py: AUTH_PASSWORD_VALIDATORS = [ | hospitalmanagement\settings.py: {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"}, | - | PARTIAL | ## 1️⃣ HTML Validation (W3C Nu Validator) |
| **Screenshot:** | No local match found | - | FAIL | ## 1️⃣ HTML Validation (W3C Nu Validator) |
| - Removed unnecessary trailing `/` from affected void elements where required. | hospital\views.py: messages.success(request, "Doctor has been rejected and removed.") | - | PARTIAL | ### Fixes Applied |
| - Moved all inline `<style>` blocks from page content sections (e.g. inside `<main>`) into the base templates’ `<head>` section. | hospital\views.py: messages.success(request, "Doctor has been rejected and removed.") | templates\hospital\aboutus.html: <style> | templates\hospital\aboutus.html: </style> | - | PARTIAL | ### Fixes Applied |
| - Re-ran the validator until **no HTML errors** were reported. | hospitalmanagement\settings.py: AUTH_PASSWORD_VALIDATORS = [ | hospitalmanagement\settings.py: {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"}, | hospitalmanagement\settings.py: {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"}, | - | PARTIAL | ### Fixes Applied |
| --- | No local match found | - | FAIL | ### Fixes Applied |
| - Downloaded `static/style.css` locally and uploaded it directly to the validator instead of validating via the dynamic Heroku path. | hospitalmanagement\settings.py: STATIC_DIR = BASE_DIR / "static" | hospitalmanagement\settings.py: "django.contrib.staticfiles", | hospitalmanagement\settings.py: "whitenoise.middleware.WhiteNoiseMiddleware",  # static files on Heroku | - | PARTIAL | ### Fixes Applied |
| - Cleaned up custom CSS where possible, keeping only necessary rules. | hospitalmanagement\settings.py: # Where STATICFILES_DIRS exists in development | hospitalmanagement\settings.py: # Where static files are collected for production (Heroku) | hospitalmanagement\urls.py: # Custom admin dashboard v2 (add-only routes) | - | PARTIAL | ### Fixes Applied |
| - Accepted vendor-prefixed rules and deprecation warnings coming from **third-party CDN stylesheets** (Bootstrap & Font Awesome). These are external dependencies and are **not modified** in this project. | ai_hub\views.py: redaction_rules = "" | ai_hub\views.py: redaction_rules = ( | ai_hub\views.py: "Redaction rules: replace any identifiers with placeholders like " | - | PARTIAL | ### Fixes Applied |
| --- | No local match found | - | FAIL | ### Fixes Applied |
| **Tool:** W3C CSS Validator (https://jigsaw.w3.org/css-validator/) | hospitalmanagement\settings.py: SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https") | hospitalmanagement\settings.py: AUTH_PASSWORD_VALIDATORS = [ | hospitalmanagement\settings.py: {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"}, | - | PARTIAL | ## 2️⃣ CSS Validation (W3C Jigsaw) |
| **Screenshot:** | No local match found | - | FAIL | ## 2️⃣ CSS Validation (W3C Jigsaw) |
| **Tool:** JSHint (https://jshint.com/) | hospitalmanagement\settings.py: SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https") | templates\hospital\adminlogin.html: <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet"> | templates\hospital\adminlogin.html: <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.2/css/all.min.css" integrity="sha512-dhnY6cnN6TqO3Y4+Q3K7S8q5bgZp3ynjTEK2XsyKMmuc/6Wn0GCLYKnrSc7hhV9x/eEwVxOUYvE2QFZ3gk9c5A==" crossorigin="anonymous" referrerpolicy="no-referrer"/> | - | PARTIAL | ## 3️⃣ JavaScript Validation (JSHint) |
| **Screenshot:** | No local match found | - | FAIL | ## 3️⃣ JavaScript Validation (JSHint) |
| - `arrow function syntax (=>) is only available in ES6` | hospitalmanagement\settings.py: # Configure Stripe SDK only if we actually have a key | hospitalmanagement\urls.py: # Custom admin dashboard v2 (add-only routes) | hospital\views.py: # Helper functions for roles | - | PARTIAL | ### Initial Warnings |
| - `const is available in ES6 (use 'esversion: 6')` | payments\views.py: event = stripe.Webhook.construct_event( | templates\hospital\admin_discharge_patient.html: <td colspan="4" class="text-center text-muted">No patients available for discharge.</td> | templates\hospital\admin_view_doctor_specialisation.html: <td colspan="4" class="text-center">No doctor specialisations available.</td> | - | PARTIAL | ### Initial Warnings |
| --- | No local match found | - | FAIL | ### Initial Warnings |
| * STRIPE keys | hospitalmanagement\settings.py: import stripe | hospitalmanagement\settings.py: "payments",  # Stripe / payments app | hospitalmanagement\settings.py: # STRIPE SETTINGS | - | PARTIAL | # 🚀 **Deployment Guide (Heroku)** |
| * SECRET_KEY | hospitalmanagement\settings.py: SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key") | hospitalmanagement\settings.py: STRIPE_SECRET_KEY = os.environ.get("STRIPE_SECRET_KEY", "") | hospitalmanagement\settings.py: if STRIPE_SECRET_KEY: | - | PARTIAL | # 🚀 **Deployment Guide (Heroku)** |
| * DEBUG | hospitalmanagement\settings.py: # Use environment variable to control DEBUG | hospitalmanagement\settings.py: # Default = True for local dev. On Heroku set DEBUG=false in Config Vars. | hospitalmanagement\settings.py: DEBUG = os.getenv("DEBUG", "True").lower() == "true" | - | PARTIAL | # 🚀 **Deployment Guide (Heroku)** |
| * ALLOWED_HOSTS | hospitalmanagement\settings.py: # ✔ ALLOWED_HOSTS — LOCAL + HEROKU APPS | hospitalmanagement\settings.py: ALLOWED_HOSTS = [ | hospitalmanagement\settings.py: for host in os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",") | - | PARTIAL | # 🚀 **Deployment Guide (Heroku)** |
| --- | No local match found | - | FAIL | # 🚀 **Deployment Guide (Heroku)** |
| --- | No local match found | - | FAIL | # 📁 File Structure |
| * **Rachel Furlong** | No local match found | - | FAIL | # 🙏 **Credits & Attribution** |
| * **Spencer Barriball** | No local match found | - | FAIL | # 🙏 **Credits & Attribution** |
| * Bootstrap | templates\hospital\adminlogin.html: <!-- Bootstrap & Font Awesome --> | templates\hospital\adminlogin.html: <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet"> | templates\hospital\adminsignup.html: <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet"> | - | PARTIAL | # 🙏 **Credits & Attribution** |
| * Django Docs | hospitalmanagement\settings.py: "django.contrib.admin", | hospitalmanagement\settings.py: "django.contrib.auth", | hospitalmanagement\settings.py: "django.contrib.contenttypes", | - | PARTIAL | # 🙏 **Credits & Attribution** |
| * Stripe Docs | hospitalmanagement\settings.py: import stripe | hospitalmanagement\settings.py: "payments",  # Stripe / payments app | hospitalmanagement\settings.py: # STRIPE SETTINGS | - | PARTIAL | # 🙏 **Credits & Attribution** |
| * Balsamiq | No local match found | - | FAIL | # 🙏 **Credits & Attribution** |
| * GitHub | No local match found | - | FAIL | # 🙏 **Credits & Attribution** |
| --- | No local match found | - | FAIL | # 🙏 **Credits & Attribution** |
| --- | No local match found | - | FAIL | # 📜 **License** |
| --- | No local match found | - | FAIL | # 🎉 **Conclusion** |

## README Asset Integrity

| Asset | Status | Git |
| ----- | ------ | --- |
| https://raw.githubusercontent.com/Purohit1999/hospital_management/main/static/images/desktop.png | EXTERNAL | Skipped |
| https://raw.githubusercontent.com/Purohit1999/hospital_management/main/static/images/tablet.png | EXTERNAL | Skipped |
| https://raw.githubusercontent.com/Purohit1999/hospital_management/main/static/images/mobile.png | EXTERNAL | Skipped |
| static/images/diagram.png | OK | tracked |
| static/images/data_flow.png | OK | tracked |
| static/images/erd.png | OK | tracked |
| https://raw.githubusercontent.com/Purohit1999/hospital_management/main/static/images/html_validate.png | EXTERNAL | Skipped |
| https://raw.githubusercontent.com/Purohit1999/hospital_management/main/static/images/css_valid.png | EXTERNAL | Skipped |
| https://raw.githubusercontent.com/Purohit1999/hospital_management/main/static/images/js_valid.png | EXTERNAL | Skipped |
| static/images/diagram.png | OK | tracked |
| static/images/data_flow.png | OK | tracked |
| static/images/erd.png | OK | tracked |

## Live Site Checks (Public Only)

| URL | Result | Notes |
| --- | ------ | ----- |
| https://hospital-management-web-4963f51d811d.herokuapp.com/ | 200 | OK |

## Gaps & Suggested Fixes

- Review any claims without repo evidence and align README to code.
- Verify public pages manually if a route requires authentication.
- Ensure all local assets are tracked in git and referenced with correct paths.
