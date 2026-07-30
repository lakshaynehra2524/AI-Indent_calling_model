"""Benchmarks the shipped TF-IDF+SVM baseline against an alternative model.

Prefers sentence-embeddings + LogisticRegression as "model B". If
sentence-transformers/torch isn't installed in this environment, falls back
to TF-IDF + LogisticRegression instead and records that substitution in the
report - the comparison methodology (same split, same metrics) is identical
either way, only model B's representation changes.
"""
import json
import time
from pathlib import Path

from sklearn.calibration import CalibratedClassifierCV
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score
from sklearn.model_selection import train_test_split
from sklearn.svm import LinearSVC

from train import load_dataset

REPORT_DIR = Path(__file__).resolve().parent / "reports"

# Model B only ships in place of the baseline if it clears this margin -
# otherwise the lighter TF-IDF+SVM stays in production.
MIN_MACRO_F1_MARGIN = 0.02


def _avg_latency_ms(predict_fn, samples):
    start = time.perf_counter()
    predict_fn(samples)
    elapsed = time.perf_counter() - start
    return (elapsed / max(len(samples), 1)) * 1000


def _evaluate_baseline(x_train, x_test, y_train, y_test):
    vectorizer = TfidfVectorizer()
    x_train_vec = vectorizer.fit_transform(x_train)
    x_test_vec = vectorizer.transform(x_test)

    model = CalibratedClassifierCV(LinearSVC(), cv=5)
    model.fit(x_train_vec, y_train)

    y_pred = model.predict(x_test_vec)
    latency = _avg_latency_ms(
        lambda s: model.predict(vectorizer.transform(s)), list(x_test)
    )

    return {
        "name": "TF-IDF + CalibratedClassifierCV(LinearSVC)",
        "accuracy": accuracy_score(y_test, y_pred),
        "macro_f1": f1_score(y_test, y_pred, average="macro"),
        "avg_latency_ms": latency,
    }


def _evaluate_embeddings(x_train, x_test, y_train, y_test):
    from sentence_transformers import SentenceTransformer

    encoder = SentenceTransformer("all-MiniLM-L6-v2")
    x_train_vec = encoder.encode(list(x_train))
    x_test_vec = encoder.encode(list(x_test))

    model = LogisticRegression(max_iter=1000)
    model.fit(x_train_vec, y_train)

    y_pred = model.predict(x_test_vec)
    latency = _avg_latency_ms(
        lambda s: model.predict(encoder.encode(list(s))), list(x_test)
    )

    return {
        "name": "sentence-embeddings (all-MiniLM-L6-v2) + LogisticRegression",
        "accuracy": accuracy_score(y_test, y_pred),
        "macro_f1": f1_score(y_test, y_pred, average="macro"),
        "avg_latency_ms": latency,
    }


def _evaluate_tfidf_logreg_fallback(x_train, x_test, y_train, y_test):
    vectorizer = TfidfVectorizer()
    x_train_vec = vectorizer.fit_transform(x_train)
    x_test_vec = vectorizer.transform(x_test)

    model = LogisticRegression(max_iter=1000)
    model.fit(x_train_vec, y_train)

    y_pred = model.predict(x_test_vec)
    latency = _avg_latency_ms(
        lambda s: model.predict(vectorizer.transform(s)), list(x_test)
    )

    return {
        "name": (
            "TF-IDF + LogisticRegression "
            "(fallback for model B - sentence-transformers unavailable here)"
        ),
        "accuracy": accuracy_score(y_test, y_pred),
        "macro_f1": f1_score(y_test, y_pred, average="macro"),
        "avg_latency_ms": latency,
    }


def _decide(baseline, model_b):
    margin = model_b["macro_f1"] - baseline["macro_f1"]

    if margin > MIN_MACRO_F1_MARGIN:
        winner = model_b
        decision = (
            f"Shipping '{model_b['name']}' - it beats the TF-IDF+SVM baseline by "
            f"{margin:.4f} macro-F1, enough to justify the extra dependency weight."
        )
    elif margin > 0:
        winner = baseline
        decision = (
            f"Shipping '{baseline['name']}' - model B edges it out by only "
            f"{margin:.4f} macro-F1, not enough to justify the extra dependency weight."
        )
    else:
        winner = baseline
        decision = (
            f"Shipping '{baseline['name']}' - it matches or beats model B "
            f"({abs(margin):.4f} macro-F1 ahead) while staying lighter."
        )

    return winner, decision


def _to_markdown(baseline, model_b, decision):
    lines = [
        "# Model comparison",
        "",
        "| Model | Accuracy | Macro F1 | Avg latency (ms/sample) |",
        "|---|---|---|---|",
        f"| {baseline['name']} | {baseline['accuracy']:.4f} | "
        f"{baseline['macro_f1']:.4f} | {baseline['avg_latency_ms']:.3f} |",
        f"| {model_b['name']} | {model_b['accuracy']:.4f} | "
        f"{model_b['macro_f1']:.4f} | {model_b['avg_latency_ms']:.3f} |",
        "",
        f"**Decision:** {decision}",
    ]
    return "\n".join(lines)


def compare():
    data = load_dataset()
    x_train, x_test, y_train, y_test = train_test_split(
        data["prompt"],
        data["intent"],
        random_state=42,
        test_size=0.2,
        stratify=data["intent"],
    )

    baseline = _evaluate_baseline(x_train, x_test, y_train, y_test)

    try:
        model_b = _evaluate_embeddings(x_train, x_test, y_train, y_test)
    except ImportError:
        model_b = _evaluate_tfidf_logreg_fallback(x_train, x_test, y_train, y_test)

    winner, decision = _decide(baseline, model_b)

    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    report = {
        "baseline": baseline,
        "model_b": model_b,
        "winner": winner["name"],
        "decision": decision,
    }
    (REPORT_DIR / "model_comparison.json").write_text(json.dumps(report, indent=2))

    markdown = _to_markdown(baseline, model_b, decision)
    (REPORT_DIR / "model_comparison.md").write_text(markdown)

    print(markdown)


if __name__ == "__main__":
    compare()
