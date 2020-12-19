import operator
from pathlib import Path
from typing import Callable, Mapping, Sequence, Union

from utils.parsing import StoreDictKeyPair

operators = {"+": operator.add, "*": operator.mul}


def precedence(op: str, ops_precedence: Mapping[str, int]) -> int:
    return ops_precedence.get(op, int(op in operators))


def evaluate(
    expression: Union[str, Sequence[str]], precedence_fn: Callable[[str], int]
) -> int:
    """Expression evaluator inspired by https://www.geeksforgeeks.org/expression-evaluation/."""
    # stack to store 1) operators and 2) values
    ops = []
    values = []

    for token in expression:

        # Current token is an opening brace, push it to 'ops'
        if token == "(":
            ops.append(token)

        # Current token is a number, push it to stack for numbers
        elif token.isdigit():

            values.append(int(token))

        # Closing brace encountered, solve entire brace
        elif token == ")":

            while len(ops) != 0 and ops[-1] != "(":
                val2 = values.pop()
                val1 = values.pop()
                op = ops.pop()

                values.append(operators[op](val1, val2))

            # pop opening brace
            ops.pop()

        # Current token is an operator
        else:

            # While top of 'ops' has same or greater precedence to current
            # token, which is an operator.
            # Apply operator on top of 'ops' to top two elements in values stack
            while len(ops) != 0 and precedence_fn(ops[-1]) >= precedence_fn(token):
                val2 = values.pop()
                val1 = values.pop()
                op = ops.pop()

                values.append(operators[op](val1, val2))

            # Push current token to 'ops'.
            ops.append(token)

    # Entire expression has been parsed at this point,
    # apply remaining ops to remaining values
    while len(ops) != 0:
        val2 = values.pop()
        val1 = values.pop()
        op = ops.pop()

        values.append(operators[op](val1, val2))

    # Top of 'values' contains result, return it
    return values[-1]


def operation_order(homework_path: Path, ops_precedence: Mapping[str, int]) -> None:

    with open(homework_path) as file:
        expressions = [line.replace(" ", "") for line in file.read().splitlines()]

    expression_values = [
        evaluate(expression, lambda op: precedence(op, ops_precedence))
        for expression in expressions
    ]
    print(
        f"The sum of the expressions on each line of the homework is {sum(expression_values)}."
    )


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="AoC 2020 - Day 18: Operation Order")
    parser.add_argument(
        "homework_path", type=Path, help="The path to the homework file to read"
    )
    parser.add_argument(
        "--ops_precedence",
        action=StoreDictKeyPair,
        default=dict(),
        metavar="OP1=PREC1,OP2=PREC2,...",
        help="The hard-coded precedence values for some operators. "
        "By default, the precedence of operators is 1 and parentheses is 0.",
    )
    args = parser.parse_args()
    operation_order(
        args.homework_path,
        {op: int(op_precedence) for op, op_precedence in args.ops_precedence.items()},
    )
