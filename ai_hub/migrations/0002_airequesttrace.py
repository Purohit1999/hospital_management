from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("ai_hub", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="AiRequestTrace",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("request_id", models.UUIDField(unique=True)),
                ("route", models.CharField(max_length=200)),
                ("operation_type", models.CharField(max_length=50)),
                ("llm_provider", models.CharField(blank=True, max_length=50)),
                ("rag_provider", models.CharField(blank=True, max_length=50)),
                ("latency_ms", models.IntegerField(default=0)),
                ("success", models.BooleanField(default=True)),
                ("error_message", models.TextField(blank=True)),
                ("metadata", models.JSONField(blank=True, default=dict)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("user", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
