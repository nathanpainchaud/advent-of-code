from pathlib import Path
from typing import Literal, Sequence, Tuple


def binary_search(
    bounds: Tuple[int, int], actions: Sequence[Literal["lower", "upper"]]
) -> int:
    min_bound, max_bound = bounds
    diff = max_bound - min_bound

    # Stop condition when we reach the last step of the binary search
    if len(actions) == 1:
        return min_bound if actions[0] == "lower" else max_bound
    else:  # Recursively continue the binary search
        mid = min_bound + (diff // 2)
        if actions[0] == "lower":
            next_bounds = min_bound, mid
        else:
            next_bounds = mid + 1, max_bound
        return binary_search(next_bounds, actions[1:])


def get_seat_id(boarding_pass: str) -> int:
    row_search = {"F": "lower", "B": "upper"}
    row = binary_search((0, 127), [row_search[half] for half in boarding_pass[:7]])
    column_search = {"L": "lower", "R": "upper"}
    column = binary_search((0, 7), [column_search[half] for half in boarding_pass[-3:]])
    return row * 8 + column


def binary_boarding(boarding_passes_path: Path) -> None:
    with open(boarding_passes_path) as file:
        boarding_passes = file.read().splitlines()

    seat_ids = [get_seat_id(boarding_pass) for boarding_pass in boarding_passes]

    # Part One
    print(f"The highest seat ID on a boarding pass is {max(seat_ids)}.")

    # Part Two
    missing_seat_id = [
        seat_id
        for seat_id in range(min(seat_ids), max(seat_ids))
        if seat_id not in seat_ids
    ]
    assert len(missing_seat_id) == 1
    print(f"Our seat ID (the empty seat) is: {missing_seat_id[0]}.")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="AoC 2020 - Day 5: Binary Boarding")
    parser.add_argument(
        "boarding_passes_path",
        type=Path,
        help="The path to the list of boarding passes to read",
    )
    args = parser.parse_args()
    binary_boarding(args.boarding_passes_path)
