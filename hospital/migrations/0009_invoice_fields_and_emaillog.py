from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("hospital", "0008_consultationrequest"),
    ]

    operations = [
        migrations.AddField(
            model_name="invoice",
            name="pdf_file",
            field=models.FileField(blank=True, null=True, upload_to="invoices/"),
        ),
        migrations.AddField(
            model_name="invoice",
            name="status",
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.CreateModel(
            name="EmailLog",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("to_email", models.EmailField(blank=True, max_length=254)),
                ("subject", models.CharField(max_length=255)),
                ("event_type", models.CharField(max_length=100)),
                ("status", models.CharField(choices=[("SUCCESS", "Success"), ("FAILED", "Failed")], max_length=10)),
                ("error_message", models.TextField(blank=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
