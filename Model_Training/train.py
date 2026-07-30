"""Reproducible training script for the intent classifier.

Regenerates linear_svc_model.pkl and tfidf_vectorizer.pkl from the dataset,
replacing the manual notebook run as the source of truth for what ships.
Also injects an explicit "unknown" class built from off-domain phrases, so
out-of-scope input has somewhere real to land instead of relying purely on
a confidence threshold over the 10 in-domain intents.
"""
import json
from pathlib import Path

import joblib
import pandas as pd
from sklearn.calibration import CalibratedClassifierCV
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score, classification_report, f1_score
from sklearn.model_selection import train_test_split
from sklearn.svm import LinearSVC

TRAINING_DIR = Path(__file__).resolve().parent
BASE_DIR = TRAINING_DIR.parent

DATASET_PATH = BASE_DIR / "Dataset" / "function_calling_ai_dataset_1500.csv"
MODEL_PATH = TRAINING_DIR / "linear_svc_model.pkl"
VECTORIZER_PATH = TRAINING_DIR / "tfidf_vectorizer.pkl"
REPORT_PATH = TRAINING_DIR / "reports" / "metrics.json"

_UNKNOWN_BASE_PHRASES = [
    "what's the weather like today",
    "tell me a joke",
    "how are you doing",
    "what is your name",
    "who won the football match last night",
    "what's the capital of france",
    "tell me a fun fact",
    "how do i make pasta",
    "what's the meaning of life",
    "translate hello into spanish",
    "what time zone is tokyo in",
    "recommend me a good movie",
    "what's happening in the news",
    "how tall is mount everest",
    "explain quantum physics simply",
    "who is the president of the united states",
    "what's 2 plus 2 in binary",
    "sing me a song",
    "what's your favorite color",
    "tell me something interesting",
    "how far is the moon from earth",
    "what year did world war two end",
    "give me a motivational quote",
    "what's the population of india",
    "how do airplanes fly",
    "what's the best programming language",
    "tell me a riddle",
    "who wrote romeo and juliet",
    "what's the stock market doing today",
    "how do i learn to swim",
]

_PREFIXES = ["", "hey ", "uh ", "please "]


def _build_unknown_rows():
    rows = [
        {"prompt": f"{prefix}{phrase}".strip(), "intent": "unknown"}
        for phrase in _UNKNOWN_BASE_PHRASES
        for prefix in _PREFIXES
    ]
    return pd.DataFrame(rows)


def load_dataset():
    known = pd.read_csv(DATASET_PATH)
    unknown = _build_unknown_rows()
    return pd.concat([known, unknown], ignore_index=True)


def train():
    data = load_dataset()

    x_train, x_test, y_train, y_test = train_test_split(
        data["prompt"],
        data["intent"],
        random_state=42,
        test_size=0.2,
        stratify=data["intent"],
    )

    vectorizer = TfidfVectorizer()
    x_train_vec = vectorizer.fit_transform(x_train)
    x_test_vec = vectorizer.transform(x_test)

    # LinearSVC has no predict_proba - CalibratedClassifierCV wraps it with
    # cross-validated probability calibration so predictor.py gets a real
    # confidence score, not just a raw label.
    model = CalibratedClassifierCV(LinearSVC(), cv=5)
    model.fit(x_train_vec, y_train)

    y_pred = model.predict(x_test_vec)
    accuracy = accuracy_score(y_test, y_pred)
    macro_f1 = f1_score(y_test, y_pred, average="macro")
    report = classification_report(y_test, y_pred, output_dict=True)

    joblib.dump(model, MODEL_PATH)
    joblib.dump(vectorizer, VECTORIZER_PATH)

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(
        json.dumps(
            {
                "model": "TF-IDF + CalibratedClassifierCV(LinearSVC)",
                "accuracy": accuracy,
                "macro_f1": macro_f1,
                "classification_report": report,
                "n_train": len(x_train),
                "n_test": len(x_test),
            },
            indent=2,
        )
    )

    print(f"accuracy={accuracy:.4f} macro_f1={macro_f1:.4f}")
    print(f"model saved to {MODEL_PATH}")
    print(f"vectorizer saved to {VECTORIZER_PATH}")
    print(f"metrics saved to {REPORT_PATH}")


if __name__ == "__main__":
    train()
