from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("hospital", "0009_invoice_fields_and_emaillog"),
    ]

    operations = [
        migrations.AddField(
            model_name="dischargedetails",
            name="is_paid",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="dischargedetails",
            name="stripe_session_id",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="dischargedetails",
            name="paid_at",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
