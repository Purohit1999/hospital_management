from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# ------------------------------------------------------------
# Doctor model
# ------------------------------------------------------------
class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    department = models.CharField(max_length=100, default='General')
    mobile = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.user:
            return f"Dr. {self.user.get_full_name()} - {self.department}"
        return f"Unassigned Doctor - {self.department}"


# ------------------------------------------------------------
# Patient model
# ------------------------------------------------------------
class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.TextField(blank=True)
    mobile = models.CharField(max_length=15, blank=True)
    symptoms = models.TextField(blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    assignedDoctorId = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.get_full_name() if self.user else "Unassigned Patient"


# ------------------------------------------------------------
# DischargeDetails model
# ------------------------------------------------------------
class DischargeDetails(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True, blank=True)
    admission_date = models.DateField()
    discharge_date = models.DateField()
    summary = models.TextField()
    room_charge = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    doctor_fee = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    medicine_cost = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    other_charge = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient.user.get_full_name()} discharged on {self.discharge_date}"


# ------------------------------------------------------------
# Appointment model (Updated)
# ------------------------------------------------------------
class Appointment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True, blank=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True, blank=True)
    date_time = models.DateTimeField(default=timezone.now)
    description = models.TextField(blank=True)  # ✅ Add this field for notes/symptoms
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='appointments_created')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='appointments_updated')

    def __str__(self):
        patient_name = self.patient.user.get_full_name() if self.patient else "Unknown Patient"
        doctor_name = f"Dr. {self.doctor.user.get_full_name()}" if self.doctor else "Unknown Doctor"
        return f"{patient_name} with {doctor_name} @ {self.date_time.strftime('%Y-%m-%d %H:%M')}"

    class Meta:
        ordering = ['-date_time']


# ------------------------------------------------------------
# Prescription model
# ------------------------------------------------------------
class Prescription(models.Model):
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE)
    date_issued = models.DateField(default=timezone.now)
    medications = models.TextField()
    instructions = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='prescriptions_created')

    def __str__(self):
        return f"Prescription for {self.appointment.patient.user.get_full_name()}"


# ------------------------------------------------------------
# Invoice model
# ------------------------------------------------------------
class Invoice(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    issued_date = models.DateField(default=timezone.now)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='invoices_created')

    def __str__(self):
        return f"Invoice #{self.id} - {self.patient.user.get_full_name()}"


# ------------------------------------------------------------
# Feedback model
# ------------------------------------------------------------
class Feedback(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    comments = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.appointment.patient.user.get_full_name()} rated {self.rating}/5"
