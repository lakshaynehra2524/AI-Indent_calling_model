from streamlit.testing.v1 import AppTest


def _find(elements, label):
    for element in elements:
        if element.label == label:
            return element
    raise AssertionError(f"no element with label {label!r}")


def test_app_loads_without_exceptions():
    at = AppTest.from_file("../app.py")
    at.run(timeout=15)
    assert not at.exception


def test_chat_command_routes_to_calculator_and_computes():
    at = AppTest.from_file("../app.py")
    at.run()

    at.chat_input[0].set_value("please open calculator").run()
    assert not at.exception
    assert at.session_state["active_section"] == "calculator"

    expression_input = _find(at.text_input, "Enter expression")
    expression_input.set_value("2 + 2 * 3").run()

    calculate_button = _find(at.button, "Calculate")
    calculate_button.click().run()

    assert not at.exception
    assert any("= 8" in element.value for element in at.success)


def test_nonsense_input_falls_back_to_home():
    at = AppTest.from_file("../app.py")
    at.run()

    at.chat_input[0].set_value("zzxq wvbn qpoiu ftmm").run()
    assert not at.exception
    assert at.session_state["active_section"] == "home"
