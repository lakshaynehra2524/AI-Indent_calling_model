from .config import CONFIDENCE_THRESHOLD

ROUTES = {
    "open_call": "call",
    "open_mail": "mail",
    "open_camera": "camera",
    "open_music": "music",
    "open_alarm": "alarm",
    "open_calculator": "calculator",
    "open_running": "running",
    "open_water_tracker": "water",
    "open_sleep_tracker": "sleep",
    "open_flashlight": "flashlight",
}


def route_intent(intent, confidence=1.0):
    """Maps a predicted intent to a UI section.

    Falls back to "home" when the label is the explicit "unknown" class
    or the model wasn't confident enough, instead of forcing a random section.
    """
    if intent == "unknown" or confidence < CONFIDENCE_THRESHOLD:
        return "home"

    return ROUTES.get(intent, "home")
