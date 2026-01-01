import json
from pathlib import Path

from django.apps import apps
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand
from django.db import transaction


DEMO_FILE = Path(__file__).resolve().parents[3] / "tools" / "demo_doctors_created.json"


class Command(BaseCommand):
    help = "Create or approve demo doctors and ensure Doctor profiles exist."

    def add_arguments(self, parser):
        parser.add_argument("--count", type=int, default=5)
        parser.add_argument("--start", type=int, default=1)
        parser.add_argument("--password", type=str, default="Test@12345")
        parser.add_argument("--approve", action="store_true")
        parser.add_argument("--repair-existing", action="store_true")
        parser.add_argument("--force-password", action="store_true")
        parser.add_argument("--delete-demo", action="store_true")

    def handle(self, *args, **options):
        doctor_model = find_doctor_model()
        if not doctor_model:
            self.stderr.write("Doctor model not found. No changes made.")
            return

        if options["delete_demo"]:
            self._delete_demo(doctor_model)
            return

        count = max(options["count"], 1)
        start = max(options["start"], 1)
        password = options["password"]
        approve = options["approve"]
        repair_existing = options["repair_existing"]
        force_password = options["force_password"]

        created_usernames = []
        summary = []

        User = get_user_model()
        doctor_user_field = find_user_field(doctor_model)
        approval_field = find_approval_field(doctor_model)
        processed = set()

        with transaction.atomic():
            if repair_existing:
                doctor_group = Group.objects.filter(name="DOCTOR").first()
                group_users = doctor_group.user_set.all() if doctor_group else []
                for user in group_users:
                    if user.username in processed:
                        continue
                    doctor_profile, created_doctor = get_or_create_doctor(
                        doctor_model, doctor_user_field, user
                    )
                    approved = False
                    if approve and doctor_profile:
                        approved = set_approved(doctor_profile, approval_field)
                    processed.add(user.username)
                    summary.append(
                        {
                            "username": user.username,
                            "created_user": False,
                            "created_doctor": created_doctor,
                            "approved": approved,
                            "notes": "repaired_profile" if created_doctor else "existing_profile",
                        }
                    )

            for i in range(start, start + count):
                username = f"doctor{i}"
                if username in processed:
                    continue
                user, created_user = User.objects.get_or_create(
                    username=username,
                    defaults={
                        "email": f"{username}@example.com",
                        "first_name": f"Demo{i}",
                        "last_name": "Doctor",
                    },
                )
                if created_user:
                    user.set_password(password)
                    user.save(update_fields=["password"])
                    created_usernames.append(username)
                elif force_password:
                    user.set_password(password)
                    user.save(update_fields=["password"])

                doctor_profile, created_doctor = get_or_create_doctor(
                    doctor_model, doctor_user_field, user
                )
                repaired = False
                if repair_existing and doctor_profile and not created_doctor:
                    repaired = True

                approved = False
                if approve and doctor_profile:
                    approved = set_approved(doctor_profile, approval_field)

                ensure_group_membership(user, "DOCTOR")

                notes = []
                if not created_user and user.username == "doctor1":
                    notes.append("existing_user")
                if doctor_profile is None:
                    notes.append("doctor_profile_missing")
                if repaired:
                    notes.append("repaired_profile")

                summary.append(
                    {
                        "username": username,
                        "created_user": created_user,
                        "created_doctor": created_doctor,
                        "approved": approved,
                        "notes": ",".join(notes) or "-",
                    }
                )
                processed.add(username)

        write_demo_file(created_usernames)
        self._print_summary(summary)

    def _delete_demo(self, doctor_model):
        User = get_user_model()
        usernames = read_demo_file()
        if not usernames:
            self.stderr.write(
                "No local demo record found. Refusing to delete without a known list."
            )
            return

        doctor_user_field = find_user_field(doctor_model)
        with transaction.atomic():
            for username in usernames:
                user = User.objects.filter(username=username).first()
                if not user:
                    continue
                if doctor_user_field:
                    doctor_model.objects.filter(**{doctor_user_field: user}).delete()
                user.delete()
        self.stdout.write("Demo doctors removed based on local demo file.")

    def _print_summary(self, summary):
        self.stdout.write("username | created_user | created_doctor_profile | approved | notes")
        for row in summary:
            self.stdout.write(
                f"{row['username']} | {row['created_user']} | "
                f"{row['created_doctor']} | {row['approved']} | {row['notes']}"
            )


def find_doctor_model():
    for model in apps.get_models():
        if model.__name__.lower() == "doctor":
            return model
    return None


def find_user_field(model):
    User = get_user_model()
    for field in model._meta.fields:
        remote = getattr(field, "remote_field", None)
        if remote and remote.model == User:
            return field.name
    return None


def find_approval_field(model):
    candidates = {"status", "approved", "is_approved", "isapproved"}
    for field in model._meta.fields:
        if field.name.lower() in candidates:
            return field
    return None


def get_or_create_doctor(model, user_field, user):
    if not user_field:
        return None, False
    obj, created = model.objects.get_or_create(**{user_field: user})
    return obj, created


def set_approved(instance, approval_field):
    if not approval_field:
        return False
    name = approval_field.name
    if hasattr(approval_field, "get_internal_type"):
        field_type = approval_field.get_internal_type()
    else:
        field_type = ""
    if field_type in {"BooleanField", "NullBooleanField"}:
        setattr(instance, name, True)
    elif field_type in {"IntegerField", "SmallIntegerField"}:
        setattr(instance, name, 1)
    else:
        setattr(instance, name, True)
    instance.save(update_fields=[name])
    return True


def ensure_group_membership(user, group_name):
    group, _ = Group.objects.get_or_create(name=group_name)
    user.groups.add(group)


def write_demo_file(usernames):
    if not usernames:
        return
    try:
        DEMO_FILE.parent.mkdir(parents=True, exist_ok=True)
        DEMO_FILE.write_text(json.dumps(usernames, indent=2), encoding="utf-8")
    except Exception:
        pass


def read_demo_file():
    try:
        if DEMO_FILE.exists():
            return json.loads(DEMO_FILE.read_text(encoding="utf-8"))
    except Exception:
        return []
    return []
