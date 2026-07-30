import re

_CALL_NAME_PATTERN = re.compile(
    r"\b(?:call|phone|ring|dial)\s+([a-zA-Z][\w'-]*)",
    re.IGNORECASE,
)
_PHONE_PATTERN = re.compile(r"\+?\d[\d\-\s]{7,}\d")

# Tried before the fallback below so "mail to john" resolves to "john", not "to"
# (the fallback alternative "mail|email" would otherwise match "mail" itself
# and capture the next word, which is "to").
_MAIL_TO_PATTERN = re.compile(r"\bto\s+([a-zA-Z][\w'-]*)", re.IGNORECASE)
_MAIL_FALLBACK_PATTERN = re.compile(
    r"\b(?:mail|email)\s+([a-zA-Z][\w'-]*)", re.IGNORECASE
)
_MAIL_ABOUT_PATTERN = re.compile(r"\babout\s+(.+)$", re.IGNORECASE)

_DURATION_PATTERN = re.compile(
    r"\bin\s+(\d+)\s*(minutes?|mins?|hours?|hrs?)\b", re.IGNORECASE
)
_ABS_TIME_PATTERN = re.compile(
    r"\bat\s+(\d{1,2})(?::(\d{2}))?\s*(am|pm)?\b", re.IGNORECASE
)

_EXPR_CHARS_PATTERN = re.compile(r"[0-9+\-*/%.() ]+")

_SONG_PATTERN = re.compile(r"\bplay\s+(.+)$", re.IGNORECASE)


def _extract_call(text):
    entities = {}

    phone_match = _PHONE_PATTERN.search(text)
    if phone_match:
        entities["phone"] = phone_match.group(0).strip()

    name_match = _CALL_NAME_PATTERN.search(text)
    if name_match:
        entities["contact"] = name_match.group(1).strip()

    return entities


def _extract_mail(text):
    entities = {}

    to_match = _MAIL_TO_PATTERN.search(text) or _MAIL_FALLBACK_PATTERN.search(text)
    if to_match:
        entities["recipient"] = to_match.group(1).strip()

    about_match = _MAIL_ABOUT_PATTERN.search(text)
    if about_match:
        entities["subject"] = about_match.group(1).strip()

    return entities


def _extract_alarm(text):
    duration_match = _DURATION_PATTERN.search(text)
    if duration_match:
        amount = int(duration_match.group(1))
        unit = duration_match.group(2).lower()
        minutes = amount * 60 if unit.startswith(("hour", "hr")) else amount
        return {"duration_minutes": minutes}

    time_match = _ABS_TIME_PATTERN.search(text)
    if time_match:
        hour = int(time_match.group(1))
        minute = int(time_match.group(2) or 0)
        meridiem = (time_match.group(3) or "").lower()

        if meridiem == "pm" and hour != 12:
            hour += 12
        if meridiem == "am" and hour == 12:
            hour = 0

        return {"hour": hour, "minute": minute}

    return {}


def _extract_calculator(text):
    candidates = _EXPR_CHARS_PATTERN.findall(text)

    for candidate in sorted(candidates, key=len, reverse=True):
        stripped = candidate.strip()
        has_digit = any(ch.isdigit() for ch in stripped)
        has_operator = any(op in stripped for op in "+-*/%")

        if stripped and has_digit and has_operator:
            return {"expression": stripped}

    return {}


def _extract_music(text):
    match = _SONG_PATTERN.search(text)
    if match:
        return {"query": match.group(1).strip()}

    return {}


_EXTRACTORS = {
    "open_call": _extract_call,
    "open_mail": _extract_mail,
    "open_alarm": _extract_alarm,
    "open_calculator": _extract_calculator,
    "open_music": _extract_music,
}


def extract_entities(text, intent):
    """Pulls slot values (contact, time, expression, ...) out of raw text.

    Intents without a registered extractor return {} - the fixed set of
    UI-only sections (camera, running, water, sleep, flashlight) have no
    slots to fill.
    """
    extractor = _EXTRACTORS.get(intent)
    if extractor is None:
        return {}

    return extractor(text)
