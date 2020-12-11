import typing
from collections import Counter
from pathlib import Path
from typing import Sequence


def compute_joltage_diff_distribution(adapters: Sequence[int]) -> typing.Counter[int]:
    adapters = list(sorted(adapters))
    joltage_diff_distribution = Counter()
    last = adapters[0]
    for adapter in adapters[1:]:
        joltage_diff_distribution[adapter - last] += 1
        last = adapter
    return joltage_diff_distribution


def count_valid_arrangements(adapters: Sequence[int]) -> int:
    adapters = list(sorted(adapters))

    memoization_table = [1]
    for cur_adapter_pos in range(1, len(adapters)):
        cur_adapter_valid_arrangements = 0
        for earlier_adapter_pos in range(cur_adapter_pos):
            if adapters[cur_adapter_pos] - adapters[earlier_adapter_pos] <= 3:
                cur_adapter_valid_arrangements += memoization_table[earlier_adapter_pos]
        memoization_table.append(cur_adapter_valid_arrangements)

    return memoization_table[-1]


def adapter_array(
    adapters_path: Path,
) -> None:
    with open(adapters_path) as file:
        adapters = [int(line) for line in file.read().splitlines()]
    adapters += [
        0,
        max(adapters) + 3,
    ]  # include the outlet and device built-in adapter in the adapters

    joltage_diffs = compute_joltage_diff_distribution(adapters)
    print(
        "The number of 1-jolt differences multiplied by the number of 3-jolt differences is "
        f"{joltage_diffs[1] * joltage_diffs[3]}."
    )

    num_arrangements = count_valid_arrangements(adapters)
    print(
        f"The total number of distinct ways that the adapters can be arranged to connect the charging outlet to the "
        f"device is {num_arrangements}."
    )


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="AoC 2020 - Day 10: Adapter Array")
    parser.add_argument(
        "adapters_path",
        type=Path,
        help="The path to the adapters joltage data file to read",
    )
    args = parser.parse_args()
    adapter_array(args.adapters_path)
