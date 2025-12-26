from django.db import migrations, models


def normalize_payment_status(apps, schema_editor):
    Payment = apps.get_model("payments", "Payment")
    Payment.objects.filter(status__iexact="paid").update(status="paid")
    Payment.objects.filter(status="succeeded").update(status="paid")


class Migration(migrations.Migration):
    dependencies = [
        ("payments", "0002_payment_fields"),
    ]

    operations = [
        migrations.AlterField(
            model_name="payment",
            name="status",
            field=models.CharField(
                choices=[
                    ("created", "Created"),
                    ("pending", "Pending"),
                    ("paid", "Paid"),
                    ("failed", "Failed"),
                ],
                default="created",
                max_length=20,
            ),
        ),
        migrations.RunPython(normalize_payment_status, migrations.RunPython.noop),
    ]
