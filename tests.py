"""
Unit tests
"""
import pytest

from main import Interpreter

interpreter = Interpreter()


def test_add_with_repl() -> None:
    assert interpreter.input("1 + 1") == 2


def test_minus_with_repl() -> None:
    assert interpreter.input("2 - 1") == 1


def test_multiply_with_repl() -> None:
    assert interpreter.input("2 * 3") == 6


def test_divide_with_repl() -> None:
    assert interpreter.input("8 / 4") == 2


def test_module_with_repl() -> None:
    assert interpreter.input("7 % 4") == 3


def test_set_variable() -> None:
    assert interpreter.input("x = 1") == 1


def test_get_existing_variable() -> None:
    assert interpreter.input("x") == 1


def test_reject_invalid_input() -> None:
    with pytest.raises(ValueError):
        interpreter.input('1 2')
