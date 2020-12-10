import itertools
from pathlib import Path
from typing import Sequence


def is_number_valid(number: int, preamble: Sequence[int]) -> bool:
    return any(
        number == sum(combination)
        for combination in itertools.combinations(preamble, 2)
    )


def compute_encryption_weakness(port_data: Sequence[int], invalid_number: int) -> int:
    # Find the range that sums to the invalid number
    weakness_ranges = [
        port_data[i : j + 1]
        for i in range(len(port_data))
        for j in range(i + 1, len(port_data))
        if sum(port_data[i : j + 1]) == invalid_number
    ]
    if len(weakness_ranges) > 1:
        raise RuntimeError(
            "Found more than one range that sums to the XMAS invalid number:",
            "\n".join(weakness_ranges),
        )
    weakness_range = weakness_ranges[0]

    # Computes the encryption weakness from the range
    return min(weakness_range) + max(weakness_range)


def encoding_error(
    port_data_path: Path,
) -> None:
    with open(port_data_path) as file:
        port_data = [int(line) for line in file.read().splitlines()]

    preamble_length = 25
    number_idx = preamble_length
    while is_number_valid(
        port_data[number_idx], port_data[number_idx - preamble_length : number_idx]
    ):
        number_idx += 1

    if number_idx == len(port_data):
        raise RuntimeError(
            "Finished scanning all data from the port without finding any invalid numbers."
        )
    print(f"{port_data[number_idx]} is the first invalid number in the port's data.")

    encryption_weakness = compute_encryption_weakness(port_data, port_data[number_idx])
    print(
        f"The encryption weakness in the XMAS-encrypted list of numbers is {encryption_weakness}."
    )


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="AoC 2020 - Day 9: Encoding Error")
    parser.add_argument(
        "port_data_path",
        type=Path,
        help="The path to the port data file to read",
    )
    args = parser.parse_args()
    encoding_error(args.port_data_path)
