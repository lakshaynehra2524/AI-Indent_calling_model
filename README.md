# AI Function-Calling Assistant



Example: `"call mom in 10 minutes"` →
```json
{"intent": "open_call", "confidence": 0.93, "entities": {"contact": "mom"}, "route": "call"}
```

> This project is local-only by design - there is no hosted/deployed version.
> Everything below runs on `localhost`.

## What's real vs. what's UI-only

| Section | Status |
|---|---|
| Calculator | Real - evaluates the expression via an AST-based safe evaluator (no `eval()`) |
| Camera | Real - captures an actual photo via `st.camera_input`, saves it locally |
| Alarm | Real - live countdown to a target time, alert + generated beep on zero |
| Call | Real (honest) - resolves a contact and renders a working `tel:` link |
| Mail | Real - sends via SMTP when configured; clear preview-only mode otherwise |
| Music | Real - lists and plays audio files from `assets/music/` |
| Analytics | Real - reads logged predictions from SQLite |
| Home, Running, Water, Sleep, Flashlight | UI-only placeholders (unchanged) |

## Architecture

```
core/          shared logic - predictor, entity extraction, router, safe math,
               contacts, SQLite logging. Imported directly by both front doors.
app.py         Streamlit UI  ──┐
api/main.py    FastAPI API   ──┴──> core/ (no HTTP call between the two - they're
                                      independent consumers of the same logic)
Model_Training/  train.py (reproducible training), compare_models.py (baseline
                  vs. alternative model), reports/ (generated comparison output)
sections/        one render() per UI section
tests/           pytest suite over core/ and api/
```

`api/main.py` is optional - it demonstrates the same intent/entity/routing
logic is usable outside Streamlit entirely (curl, Postman, a future client),
not something the Streamlit app depends on at runtime.

## Model

TF-IDF + `LinearSVC`, wrapped in `CalibratedClassifierCV` so predictions come
with a real calibrated confidence score (`predict_proba`) instead of a raw
decision-function margin. An explicit `unknown` class (off-domain phrases
like "what's the weather today") gives out-of-scope input somewhere real to
land; predictions below `CONFIDENCE_THRESHOLD` (see `core/config.py`) also
fall back to Home rather than forcing a random section.

`Model_Training/compare_models.py` benchmarks this baseline against a second
model (sentence-embeddings + `LogisticRegression`, or a lighter TF-IDF +
`LogisticRegression` fallback if `sentence-transformers` isn't installed) on
accuracy, macro-F1, and per-sample latency, and writes the verdict to
`Model_Training/reports/model_comparison.md`.

## Setup

```bash
pip install -r requirements.txt
```

Training/benchmarking/testing extras (not needed just to run the app):

```bash
pip install -r Model_Training/requirements-train.txt
```

Optional, for real email sending:

```bash
cp .env.example .env   # then fill in your SMTP credentials
```

## Running it

```bash
# Regenerate the model (only needed after changing the dataset/pipeline)
python Model_Training/train.py

# Compare the baseline against the alternative model
python Model_Training/compare_models.py

# Run tests
pytest

# Run the app
streamlit run app.py

# Optional: run the API independently
uvicorn api.main:app --reload
```

Try: `"call mom"`, `"set an alarm in 10 minutes"`, `"5 * (3 + 2)"`,
`"mail to john about the report"`, `"play some jazz"`, and a nonsense phrase
to see the low-confidence fallback to Home.

## Tests

`pytest` covers `core/` (predictor, entity extraction, router, safe math),
the FastAPI endpoints via `TestClient`, and three Streamlit `AppTest`-driven
UI tests that actually run `app.py` end-to-end (a chat command routing to a
section and computing a real result, and the low-confidence fallback).
