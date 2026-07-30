import joblib

from .config import MODEL_PATH, VECTORIZER_PATH

_model = joblib.load(MODEL_PATH)
_vectorizer = joblib.load(VECTORIZER_PATH)


def predict_intent(text):
    """Predicts intent with a calibrated confidence score.

    Returns (intent, confidence) where confidence is the model's
    predicted probability for the winning class, in [0, 1].
    """
    vector = _vectorizer.transform([text])
    probabilities = _model.predict_proba(vector)[0]
    best_index = probabilities.argmax()

    intent = _model.classes_[best_index]
    confidence = float(probabilities[best_index])

    return intent, confidence
