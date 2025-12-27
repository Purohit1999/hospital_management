from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, User

from hospital.models import Doctor, Patient


class Command(BaseCommand):
    help = "Seed demo patients for assessment (idempotent)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--count",
            type=int,
            default=5,
            help="Number of demo patients to create (default: 5).",
        )
        parser.add_argument(
            "--password",
            type=str,
            default="Test@12345",
            help="Password for created demo users (default: Test@12345).",
        )

    def handle(self, *args, **options):
        count = options["count"]
        password = options["password"]

        created_users = []
        created_patients = []

        group, _ = Group.objects.get_or_create(name="PATIENT")
        first_doctor = Doctor.objects.order_by("id").first()

        patient_fields = {f.name for f in Patient._meta.get_fields()}
        has_assigned_doctor = "assignedDoctorId" in patient_fields
        has_status = "status" in patient_fields
        has_address = "address" in patient_fields
        has_symptoms = "symptoms" in patient_fields
        has_mobile = "mobile" in patient_fields

        for i in range(1, count + 1):
            username = f"demo_patient_{i}"
            email = f"demo_patient_{i}@example.com"
            first_name = "Demo"
            last_name = f"Patient{i}"
            address = f"{i} Demo Street"
            mobile = f"555000{i:03d}"
            symptoms = f"Demo symptoms {i}"

            user, user_created = User.objects.get_or_create(
                username=username,
                defaults={"email": email, "first_name": first_name, "last_name": last_name},
            )
            if user_created:
                user.set_password(password)
                user.save()
                created_users.append(username)

            user.groups.add(group)

            patient_defaults = {}
            if has_address:
                patient_defaults["address"] = address
            if has_mobile:
                patient_defaults["mobile"] = mobile
            if has_symptoms:
                patient_defaults["symptoms"] = symptoms
            if has_status:
                patient_defaults["status"] = False
            if has_assigned_doctor and first_doctor:
                patient_defaults["assignedDoctorId"] = first_doctor

            patient, patient_created = Patient.objects.get_or_create(
                user=user, defaults=patient_defaults
            )
            if patient_created:
                created_patients.append((username, patient.id))

        total_patients = Patient.objects.count()
        last_usernames = list(
            Patient.objects.select_related("user")
            .order_by("-id")
            .values_list("user__username", flat=True)[:10]
        )

        self.stdout.write(self.style.SUCCESS("Demo patient seeding complete."))
        self.stdout.write(f"Users created: {len(created_users)}")
        self.stdout.write(f"Patients created: {len(created_patients)}")
        self.stdout.write(f"Total patients: {total_patients}")
        self.stdout.write("Last 10 patient usernames:")
        for username in last_usernames:
            self.stdout.write(f"- {username}")
