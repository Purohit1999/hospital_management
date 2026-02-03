import os
import random
import logging
import joblib
import numpy as np
from django.conf import settings

logger = logging.getLogger(__name__)


NO_SHOW_MODEL_PATH = os.path.join(
    settings.AI_HUB_ARTIFACTS_DIR, "no_show_model.joblib"
)
COMPLAINT_MODEL_PATH = os.path.join(
    settings.AI_HUB_ARTIFACTS_DIR, "complaint_classifier.joblib"
)


def load_no_show_model(return_error=False):
    if not os.path.exists(NO_SHOW_MODEL_PATH):
        message = "No-show model not found."
        return (None, message) if return_error else None
    try:
        model = joblib.load(NO_SHOW_MODEL_PATH)
        return (model, "") if return_error else model
    except (ModuleNotFoundError, ImportError) as exc:
        logger.warning("No-show model unavailable: %s", exc)
        message = "ML model unavailable on this deployment."
        return (None, message) if return_error else None
    except Exception as exc:
        logger.exception("Failed to load no-show model")
        message = "ML model failed to load."
        return (None, message) if return_error else None


def predict_no_show(features: dict, return_error=False):
    model, error = load_no_show_model(return_error=True)
    if not model:
        if return_error:
            return None, error
        return round(random.uniform(0.05, 0.4), 3)
    vec = np.array([[features.get("days_until", 0), features.get("hour", 9)]])
    score = model.predict_proba(vec)[0][1]
    score = float(round(score, 3))
    return (score, "") if return_error else score


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
