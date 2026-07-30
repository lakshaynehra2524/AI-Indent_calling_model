from core.predictor import predict_intent

_KNOWN_INTENTS = {
    "open_call",
    "open_mail",
    "open_camera",
    "open_music",
    "open_alarm",
    "open_calculator",
    "open_running",
    "open_water_tracker",
    "open_sleep_tracker",
    "open_flashlight",
    "unknown",
}


def test_predict_returns_known_label_and_valid_confidence():
    intent, confidence = predict_intent("call mom right now")

    assert intent in _KNOWN_INTENTS
    assert 0.0 <= confidence <= 1.0


def test_predict_call_intent_for_clear_call_phrase():
    intent, _ = predict_intent("please call my mom")
    assert intent == "open_call"


def test_predict_unknown_for_off_domain_phrase():
    intent, _ = predict_intent("what's the weather like today")
    assert intent == "unknown"
