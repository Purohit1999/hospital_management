
---

## 👤 User Stories

---

### ✅ User Stories for Hospital Management System

This document outlines user stories for a Hospital Management System, focusing on the needs of **Admins**, **Doctors**, and **Patients**. The aim is to deliver a secure, intuitive platform to manage appointments, patient data, medical reports, and communication between users.

---

### 🧑‍⚕️ As an **Admin**, I want to:

#### 1. 🟢 **Register or Approve** doctors and patients.

Ensure proper onboarding of verified professionals and patients, with admin-controlled access.

#### 2. 📝 **Add and manage** appointments.

Create, approve, reject, or cancel appointments based on availability and status.

#### 3. 🔍 **View and update** doctor/patient details.

Quickly access, update, or delete user records as needed with validation and confirmation prompts.

#### 4. 🧾 **Generate discharge summaries and invoices.**

Generate PDFs for discharges and billing with cost breakdowns for room, consultation, and medicine.

#### 5. 📊 **View dashboards** for hospital stats.

See quick summaries of active doctors, admitted patients, and upcoming appointments.

#### 6. 🔒 Ensure **role-based access** to system features.

Control who can view, modify, or delete sensitive data using Django’s authentication system.

---

### 🩺 As a **Doctor**, I want to:

#### 1. 📅 **View all my appointments** by date.

Filter appointments by patient or date to manage schedules efficiently.

#### 2. 🧍‍♂️ **Access patient records** securely.

See assigned patient data, symptoms, history, and profile pictures in a single view.

#### 3. 💊 **Write and issue prescriptions** after consultations.

Add diagnoses, medication instructions, and download/print for patients.

#### 4. 🗂️ **View past discharge summaries.**

Helps in reviewing previous treatments or hospitalization cases for returning patients.

#### 5. 🛡️ Be restricted to my patients only.

Only see data related to assigned patients, maintaining confidentiality.

---

### 🧑‍🦽 As a **Patient**, I want to:

#### 1. ✅ **Register quickly** with basic info and symptoms.

Upload profile photo, enter address, mobile number, and assigned doctor if known.

#### 2. 📅 **Book appointments** with doctors of choice.

Choose preferred date/time from available slots and see confirmation status.

#### 3. 🔎 **View my upcoming and past appointments.**

See history of visits with doctor name, date/time, and appointment status.

#### 4. 📄 **Access discharge and billing info** securely.

Download hospital discharge summaries and invoices issued by staff.

#### 5. 💬 **Give feedback** after appointments.

Rate experience and provide optional comments for improvement.

---

### ✅ This system emphasizes robust **CRUD** operations for all users:

* **C**reate → Register, add appointments, prescriptions, discharge records
* **R**ead → View patients, appointments, dashboards, billing
* **U**pdate → Edit records or update statuses
* **D**elete → Remove patients, appointments, or old records (admin only)

## 📐 Wireframe Diagrams

### 🖥️ Desktop View  
![Desktop Wireframe](https://github.com/Purohit1999/hospital_management/blob/main/static/images/desktop.png?raw=true)

### 📱 Tablet View  
![Tablet Wireframe](https://github.com/Purohit1999/hospital_management/blob/main/static/images/tablet.png?raw=true)

### 📲 Mobile View  
![Mobile Wireframe](https://github.com/Purohit1999/hospital_management/blob/main/static/images/mobile.png?raw=true)

## 🧭 Data Flow Diagram

![Data Flow](https://github.com/Purohit1999/hospital_management/blob/main/static/images/data_flow.png?raw=true)
