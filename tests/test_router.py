from core.router import route_intent


def test_route_known_intent_with_high_confidence():
    assert route_intent("open_call", 0.9) == "call"


def test_route_unknown_intent_falls_back_home():
    assert route_intent("unknown", 0.9) == "home"


def test_route_low_confidence_falls_back_home():
    assert route_intent("open_call", 0.1) == "home"


def test_route_unmapped_intent_falls_back_home():
    assert route_intent("something_not_in_routes", 0.9) == "home"
