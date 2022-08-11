import re
from typing import Optional, Union


def tokenize(expression):
    if expression == "":
        return []

    regex = re.compile("\s*(=>|[-+*\/\%=\(\)]|[A-Za-z_][A-Za-z0-9_]*|[0-9]*\.?[0-9]+)\s*")
    tokens = regex.findall(expression)
    return [s for s in tokens if not s.isspace()]


class Interpreter:
    def __init__(self):
        self.vars = {}
        self.functions = {
            '+': self.add,
            '-': self.minus,
            '*': self.multiply,
            '/': self.divide,
            '%': self.module,
            '=': self.init_var,
            None: self.retrieve_var
        }

    def init_var(self, name, value):
        try:
            value = int(value)
        except ValueError:
            # if not int - just move on
            pass

        self.vars[name] = value
        return value

    def retrieve_var(self, name) -> Union[int, str]:
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

        result = ''

        if len(tokens) == 1:
            # if REPL have request for var retrieve - have separate branch
            return self.retrieve_var(tokens[0])

        if not set(self.functions).intersection(tokens):
            raise ValueError

        for index, token in enumerate(tokens):
            if token in self.functions:
                result = self.functions[token](tokens[index-1], tokens[index + 1])
                tokens[index-1:index+2] = str(result)

        return result
