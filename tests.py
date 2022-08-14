"""
Unit tests
"""
import pytest

from main import Interpreter

interpreter = Interpreter()


def test_empty_input() -> None:
    assert interpreter.input("") == ""


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
        interpreter.input("1 2")


def test_multiply_operations_1() -> None:
    assert interpreter.input("4 + 2 * 3") == 10


def test_multiply_operations_2() -> None:
    assert interpreter.input("4 / 2 * 3") == 6


def test_multiply_operations_3() -> None:
    assert interpreter.input("7 % 2 * 8") == 8


def test_multiply_with_parenthesis() -> None:
    assert interpreter.input("(4 + 2) * 3") == 18


def test_multiply_with_nested_parenthesis() -> None:
    assert interpreter.input("(8 - (4 + 2)) * 3") == 6


def test_handle_var_in_expression_1() -> None:
    assert interpreter.input("x + 3") == 4


def test_handle_var_in_expression_2() -> None:
    with pytest.raises(Exception):
        assert interpreter.input("y")


def test_assignment_in_expression() -> None:
    assert interpreter.input("y = x + 5")


def test_assigned_var() -> None:
    assert interpreter.input("y") == 6
