from django.core.management.base import BaseCommand
from django.core.mail import EmailMessage
from django.conf import settings


class Command(BaseCommand):
    help = "Send a test email to verify SMTP configuration."

    def add_arguments(self, parser):
        parser.add_argument("to_email", help="Recipient email address")

    def handle(self, *args, **options):
        to_email = options["to_email"]
        try:
            email = EmailMessage(
                subject="Hospital SMTP smoketest",
                body="This is a test email from Hospital Management.",
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[to_email],
            )
            sent = email.send(fail_silently=False)
            if sent and sent > 0:
                self.stdout.write(self.style.SUCCESS("Email sent successfully."))
            else:
                self.stdout.write(self.style.ERROR("Email send returned 0."))
        except Exception as exc:
            self.stdout.write(self.style.ERROR(f"Email send failed: {exc}"))
