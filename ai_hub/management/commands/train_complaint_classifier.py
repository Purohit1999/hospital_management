import os
import joblib
from django.core.management.base import BaseCommand
from django.conf import settings
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline


class Command(BaseCommand):
    help = "Train a simple complaint-to-department classifier."

    def handle(self, *args, **options):
        texts = [
            "chest pain and shortness of breath",
            "heart palpitations and dizziness",
            "skin rash and itching",
            "eczema flare",
            "stomach pain and nausea",
            "acid reflux and indigestion",
            "knee pain after fall",
            "back pain and stiffness",
            "headache and blurry vision",
            "severe migraine",
        ]
        labels = [
            "Cardiology",
            "Cardiology",
            "Dermatology",
            "Dermatology",
            "Gastroenterology",
            "Gastroenterology",
            "Orthopedics",
            "Orthopedics",
            "Neurology",
            "Neurology",
        ]

        model = Pipeline(
            [
                ("tfidf", TfidfVectorizer(stop_words="english")),
                ("clf", LogisticRegression(max_iter=200)),
            ]
        )
        model.fit(texts, labels)

        os.makedirs(settings.AI_HUB_ARTIFACTS_DIR, exist_ok=True)
        path = os.path.join(
            settings.AI_HUB_ARTIFACTS_DIR, "complaint_classifier.joblib"
        )
        joblib.dump(model, path)
        self.stdout.write(f"Saved model to {path}")
