import re
from typing import Dict, List, Optional, Tuple, Union


def tokenize(expression: str) -> List[str]:
    if expression == "":
        return []

    regex = re.compile(r"\s*(=>|[-+*\/\%=\(\)]|[A-Za-z_][A-Za-z0-9_]*|[0-9]*\.?[0-9]+)\s*")
    tokens = regex.findall(expression)
    return [s for s in tokens if not s.isspace()]


class Interpreter:
    def __init__(self) -> None:
        self.functions = {
            "%": self.module,
            "/": self.divide,
            "*": self.multiply,
            "+": self.add,
            "-": self.minus,
            "=": self.init_var,
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

    def parse_value(self, value: str) -> int:
        if value in self.vars:
            return int(self.vars[value])

        return int(value)

    def add(self, first: str, second: str) -> int:
        return self.parse_value(first) + self.parse_value(second)

    def minus(self, first: str, second: str) -> int:
        return self.parse_value(first) - self.parse_value(second)

    def multiply(self, first: str, second: str) -> int:
        return self.parse_value(first) * self.parse_value(second)

    def divide(self, first: str, second: str) -> float:
        return self.parse_value(first) / self.parse_value(second)

    def module(self, first: str, second: str) -> int:
        return self.parse_value(first) % self.parse_value(second)

    @staticmethod
    def parse_parenthesis(tokens: List[str]) -> Tuple[int, int]:
        count_open = 0
        count_close = 0

        index_open = []
        index_close = []

        for index, token in enumerate(tokens):
            if token == "(":
                index_open.append(index)
                count_open += 1
            elif token == ")":
                index_close.append(index)
                count_close += 1
            else:
                continue

            if index_close and count_open == count_close:
                return index_open[0], index_close[-1]

        raise ValueError

    def input(self, expression: str) -> Union[int, str]:
        tokens: List[str] = tokenize(expression)

        if not tokens:
            return ""

        if len(tokens) == 1:
            var_: str = tokens[0]
            # if REPL have request for var retrieve - have separate branch
            return self.vars[var_]

        if not set(self.functions).intersection(tokens):
            raise ValueError

        index = 0
        operators = iter(self.functions)
        operator = next(operators)

        while len(tokens) > 1:
            try:
                open_, close_ = self.parse_parenthesis(tokens)
                tokens[open_ : close_ + 1] = [str(self.input(" ".join(tokens[open_ + 1 : close_])))]
            except ValueError:
                pass

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
