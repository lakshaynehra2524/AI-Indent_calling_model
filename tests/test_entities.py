from core.entities import extract_entities


def test_extract_call_contact():
    entities = extract_entities("call mom please", "open_call")
    assert entities.get("contact") == "mom"


def test_extract_call_phone_number():
    entities = extract_entities("call 555-123-4567", "open_call")
    assert entities.get("phone") == "555-123-4567"


def test_extract_mail_recipient_and_subject():
    entities = extract_entities("mail to john about the report", "open_mail")
    assert entities.get("recipient") == "john"
    assert entities.get("subject") == "the report"


def test_extract_mail_without_to_keyword():
    entities = extract_entities("email john about the meeting", "open_mail")
    assert entities.get("recipient") == "john"


def test_extract_alarm_relative_duration():
    entities = extract_entities("set an alarm in 15 minutes", "open_alarm")
    assert entities.get("duration_minutes") == 15


def test_extract_alarm_absolute_time_pm():
    entities = extract_entities("wake me up at 7 pm", "open_alarm")
    assert entities.get("hour") == 19
    assert entities.get("minute") == 0


def test_extract_calculator_expression():
    entities = extract_entities("what is 5 + 3 * 2", "open_calculator")
    assert entities.get("expression", "").replace(" ", "") == "5+3*2"


def test_extract_music_query():
    entities = extract_entities("play some jazz", "open_music")
    assert entities.get("query") == "some jazz"


def test_extract_no_entities_for_unmapped_intent():
    assert extract_entities("turn on flashlight", "open_flashlight") == {}
