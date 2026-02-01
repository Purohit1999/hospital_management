from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("hospital", "0010_discharge_payment_fields"),
    ]

    operations = [
        migrations.AddField(
            model_name="patient",
            name="email",
            field=models.EmailField(blank=True, null=True, max_length=254),
        ),
    ]
