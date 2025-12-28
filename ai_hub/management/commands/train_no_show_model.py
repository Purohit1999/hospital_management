import os
import numpy as np
import joblib
from django.core.management.base import BaseCommand
from django.conf import settings
from sklearn.linear_model import LogisticRegression


class Command(BaseCommand):
    help = "Train a simple no-show risk model (synthetic data)."

    def handle(self, *args, **options):
        rng = np.random.default_rng(42)
        days_until = rng.integers(0, 30, size=500)
        hour = rng.integers(8, 18, size=500)
        # Simple synthetic target: higher risk for short notice and late hours
        y = ((days_until < 2) | (hour > 16)).astype(int)
        X = np.column_stack([days_until, hour])

        model = LogisticRegression()
        model.fit(X, y)

        os.makedirs(settings.AI_HUB_ARTIFACTS_DIR, exist_ok=True)
        path = os.path.join(settings.AI_HUB_ARTIFACTS_DIR, "no_show_model.joblib")
        joblib.dump(model, path)
        self.stdout.write(f"Saved model to {path}")
