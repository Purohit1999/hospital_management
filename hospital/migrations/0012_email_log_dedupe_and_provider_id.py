from django.db import migrations, models
from django.db.models import Q


class Migration(migrations.Migration):
    dependencies = [
        ("hospital", "0011_patient_email"),
    ]

    operations = [
        migrations.AddField(
            model_name="emaillog",
            name="dedupe_key",
            field=models.CharField(blank=True, db_index=True, max_length=128),
        ),
        migrations.AddField(
            model_name="emaillog",
            name="provider_message_id",
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddConstraint(
            model_name="emaillog",
            constraint=models.UniqueConstraint(
                fields=["dedupe_key"],
                condition=Q(status="PENDING") & ~Q(dedupe_key=""),
                name="uniq_emaillog_pending_dedupe_key",
            ),
        ),
    ]
