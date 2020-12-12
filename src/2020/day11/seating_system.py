import itertools
from pathlib import Path
from typing import Literal, Tuple

import numpy as np


def apply_one_round(
    seats_layout: np.ndarray, neighbours: Literal["immediate", "next"]
) -> np.ndarray:
    nb_rows, nb_cols = seats_layout.shape

    def count_occupied_immediate_neighbours(pos: Tuple[int, int]) -> int:
        row, col = pos
        patch = seats_layout[
            max(0, row - 1) : min(nb_rows, row + 2),
            max(0, col - 1) : min(nb_cols, col + 2),
        ]
        return (patch == "#").sum() - (seats_layout[pos] == "#")

    def count_occupied_next_neighbours(pos: Tuple[int, int]) -> int:
        row, col = pos
        nb_occupied_neighbours = 0
        for row_dir, col_dir in itertools.product((1, 0, -1), repeat=2):
            if not (row_dir or col_dir):
                continue
            neighbour_row, neighbour_col = row + row_dir, col + col_dir
            while 0 <= neighbour_row < nb_rows and 0 <= neighbour_col < nb_cols:
                if (neighbour := seats_layout[neighbour_row, neighbour_col]) != ".":
                    if neighbour == "#":
                        nb_occupied_neighbours += 1
                    break
                neighbour_row += row_dir
                neighbour_col += col_dir
        return nb_occupied_neighbours

    neighbour_count_fn = locals()[f"count_occupied_{neighbours}_neighbours"]
    neighbour_limit = 4 if neighbours == "immediate" else 5

    def update_pos(pos: Tuple[int, int]) -> str:
        old_pos_val = seats_layout[pos]
        new_pos_val = old_pos_val
        occupied_neighbours = neighbour_count_fn(pos)
        if old_pos_val == "L" and not occupied_neighbours:
            new_pos_val = "#"
        elif old_pos_val == "#" and occupied_neighbours >= neighbour_limit:
            new_pos_val = "L"
        return new_pos_val

    return np.array(
        [update_pos(pos) for pos in np.ndindex(seats_layout.shape)]
    ).reshape(seats_layout.shape)


def seating_system(
    seats_layout_path: Path, neighbours: Literal["immediate", "next"]
) -> None:
    with open(seats_layout_path) as file:
        seats_layout = np.array([[*line] for line in file.read().splitlines()])

    while (
        (next_layout := apply_one_round(seats_layout, neighbours)) != seats_layout
    ).any():
        seats_layout = next_layout

    num_seats_occupied = sum(pos == "#" for row in seats_layout for pos in row)
    print(
        f"{num_seats_occupied} seats end up occupied when no more seats change state."
    )


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="AoC 2020 - Day 11: Seating System")
    parser.add_argument(
        "seats_layout_path",
        type=Path,
        help="The path to the seats layout file to read",
    )
    parser.add_argument("neighbours", type=str, choices=["immediate", "next"])
    args = parser.parse_args()
    seating_system(args.seats_layout_path, args.neighbours)
