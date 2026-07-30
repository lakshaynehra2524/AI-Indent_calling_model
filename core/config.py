import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")

MODEL_DIR = BASE_DIR / "Model_Training"
MODEL_PATH = MODEL_DIR / "linear_svc_model.pkl"
VECTORIZER_PATH = MODEL_DIR / "tfidf_vectorizer.pkl"

# Below this predicted-class probability, route_intent() falls back to "home"
# instead of forcing a section the model isn't actually confident about.
CONFIDENCE_THRESHOLD = 0.35

DB_PATH = BASE_DIR / "data" / "predictions.db"

CAPTURES_DIR = BASE_DIR / "captures"
MUSIC_DIR = BASE_DIR / "assets" / "music"

SMTP_HOST = os.getenv("SMTP_HOST", "")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASS = os.getenv("SMTP_PASS", "")
SMTP_FROM = os.getenv("SMTP_FROM", SMTP_USER)


def smtp_configured():
    return bool(SMTP_HOST and SMTP_USER and SMTP_PASS)
