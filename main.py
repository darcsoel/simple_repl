import re
from typing import Dict, List, Optional, Union


def tokenize(expression: str) -> List[str]:
    if expression == "":
        return []

    regex = re.compile(r"\s*(=>|[-+*\/\%=\(\)]|[A-Za-z_][A-Za-z0-9_]*|[0-9]*\.?[0-9]+)\s*")
    tokens = regex.findall(expression)
    return [s for s in tokens if not s.isspace()]


class Interpreter:
    def __init__(self) -> None:
        self.functions = {
            "=": self.init_var,
            "%": self.module,
            "/": self.divide,
            "*": self.multiply,
            "+": self.add,
            "-": self.minus,
            None: self.retrieve_var,
        }
        self.vars: Dict[str, Union[int, str]] = {}
        self.priority = ["*", "/", "%"]

    def init_var(self, name: str, value: Union[int, str]) -> Union[int, str]:
        try:
            value = int(value)
        except ValueError:
            # if not int - just move on
            pass

        self.vars[name] = value
        return value

    def retrieve_var(self, name: str) -> Union[int, str]:
        try:
            return self.vars[name]
        except KeyError:
            return f"Invalid identifier. No variable with name '{name}' was found."

    @staticmethod
    def add(first: str, second: str) -> int:
        return int(first) + int(second)

    @staticmethod
    def minus(first: str, second: str) -> int:
        return int(first) - int(second)

    @staticmethod
    def multiply(first: str, second: str) -> int:
        return int(first) * int(second)

    @staticmethod
    def divide(first: str, second: str) -> float:
        return int(first) / int(second)

    @staticmethod
    def module(first: str, second: str) -> int:
        return int(first) % int(second)

    def input(self, expression: str) -> Optional[Union[int, float, str]]:
        tokens = tokenize(expression)

        if not tokens:
            return ""

        if len(tokens) == 1:
            # if REPL have request for var retrieve - have separate branch
            return self.retrieve_var(tokens[0])

        if not set(self.functions).intersection(tokens):
            raise ValueError

        index = 0
        operators = iter(self.functions)
        operator = next(operators)

        while len(tokens) > 1:
            token = tokens[index]

            if operator in tokens:
                if token != operator:
                    index += 1
                    continue
                else:
                    func = self.functions[operator]
                    tokens[index - 1 : index + 2] = [func(tokens[index - 1], tokens[index + 1])]  # type: ignore
                    index = 0
            else:
                operator = next(operators)

        return tokens[0]
