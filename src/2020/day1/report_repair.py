import functools
import itertools
from operator import mul
from pathlib import Path


def report_repair(expense_report: Path, combinations_length: int) -> None:
    with open(expense_report) as file:
        expense_report_vals = [int(line) for line in file.read().splitlines()]
    for vals in itertools.combinations(expense_report_vals, combinations_length):
        if sum(vals) == 2020:
            print(
                f"Values {vals} sum to 2020 and multiplied give {functools.reduce(mul, vals)}"
            )


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="AoC 2020 - Day 1: Report Repair")
    parser.add_argument(
        "report_path", type=Path, help="The path to the report file to read"
    )
    parser.add_argument(
        "combinations_length",
        type=int,
        help="The length of combinations of expenses to consider",
    )
    args = parser.parse_args()
    report_repair(args.report_path, args.combinations_length)
