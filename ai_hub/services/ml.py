import os
import random
import joblib
import numpy as np
from django.conf import settings


NO_SHOW_MODEL_PATH = os.path.join(
    settings.AI_HUB_ARTIFACTS_DIR, "no_show_model.joblib"
)
COMPLAINT_MODEL_PATH = os.path.join(
    settings.AI_HUB_ARTIFACTS_DIR, "complaint_classifier.joblib"
)


def load_no_show_model():
    if not os.path.exists(NO_SHOW_MODEL_PATH):
        return None
    return joblib.load(NO_SHOW_MODEL_PATH)


def predict_no_show(features: dict) -> float:
    model = load_no_show_model()
    if not model:
        return round(random.uniform(0.05, 0.4), 3)
    vec = np.array([[features.get("days_until", 0), features.get("hour", 9)]])
    score = model.predict_proba(vec)[0][1]
    return float(round(score, 3))


def load_complaint_classifier():
    if not os.path.exists(COMPLAINT_MODEL_PATH):
        return None
    return joblib.load(COMPLAINT_MODEL_PATH)


def predict_department(text: str):
    model = load_complaint_classifier()
    if not model:
        return "General", 0.5
    pred = model.predict([text])[0]
    proba = max(model.predict_proba([text])[0])
    return pred, float(round(proba, 3))
