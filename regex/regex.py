from dataclasses import dataclass
from typing import Dict


@dataclass
class Operator:

    name: str
    precedence: int
    left_associative: bool


class Regex:

    __operators: Dict[str, Operator] = {
        "+": Operator("+", 2, True),
        ",": Operator(",", 3, True),
        "*": Operator("*", 4, True),
        "(": Operator("(", 0, True)
    }

    def to_postfix(self, infix: str):
        # Adapted from https://en.wikipedia.org/wiki/Shunting_yard_algorithm

        transformed_infix = ""
        for i, token in enumerate(infix):
            if token in self.__operators:
                transformed_infix = transformed_infix[:-1]
                transformed_infix += token
            else:
                transformed_infix += token
                transformed_infix += ","
        infix = transformed_infix

        output_queue = []
        operator_stack = []

        i = 0

        for token in infix:
            if token.isalnum():
                output_queue.append(token)
            elif token == "(":
                operator_stack.append(token)
            elif token == ")":
                while operator_stack[-1] != "(":
                    if len(operator_stack) == 0:
                        raise Exception("Bad parentheses")
                    output_queue.append(operator_stack.pop())
                operator_stack.pop()
            elif token in self.__operators:
                precedence = self.__operators[token].precedence
                while True:
                    if len(operator_stack) == 0:
                        break
                    top = operator_stack[-1]
                    if precedence < self.__operators[top].precedence:
                        output_queue.append(top)
                        operator_stack.pop()
                    else:
                        break
                operator_stack.append(token)
        output_queue.extend(reversed(operator_stack))
        print(output_queue)

