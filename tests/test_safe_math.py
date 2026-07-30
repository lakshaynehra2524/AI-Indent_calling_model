import pytest

from core.safe_math import UnsafeExpressionError, safe_eval


def test_basic_arithmetic():
    assert safe_eval("2 + 3") == 5
    assert safe_eval("10 / 2") == 5
    assert safe_eval("2 ** 3") == 8
    assert safe_eval("7 % 2") == 1


def test_operator_precedence_and_parens():
    assert safe_eval("2 + 3 * 4") == 14
    assert safe_eval("(2 + 3) * 4") == 20


def test_unary_minus():
    assert safe_eval("-5 + 10") == 5


def test_rejects_name_based_payload():
    with pytest.raises(UnsafeExpressionError):
        safe_eval("__import__('os').system('echo hi')")


def test_rejects_function_calls():
    with pytest.raises(UnsafeExpressionError):
        safe_eval("print(1)")


def test_rejects_attribute_access():
    with pytest.raises(UnsafeExpressionError):
        safe_eval("().__class__")


def test_rejects_invalid_syntax():
    with pytest.raises(UnsafeExpressionError):
        safe_eval("2 +")
