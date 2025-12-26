from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("hospital", "0007_patient_status"),
        ("payments", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="payment",
            name="patient",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=models.deletion.CASCADE,
                related_name="payments",
                to="hospital.patient",
            ),
        ),
        migrations.AddField(
            model_name="payment",
            name="discharge",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=models.deletion.SET_NULL,
                related_name="payments",
                to="hospital.dischargedetails",
            ),
        ),
        migrations.AddField(
            model_name="payment",
            name="currency",
            field=models.CharField(default="gbp", max_length=10),
        ),
        migrations.AddField(
            model_name="payment",
            name="stripe_session_id",
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
