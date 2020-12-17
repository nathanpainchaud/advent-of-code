from pathlib import Path
from typing import Tuple

import numpy as np


def conway_cubes(initial_state_path: Path, num_dims: int) -> None:

    with open(initial_state_path) as file:
        initial_state = np.array(
            [[cube == "#" for cube in line] for line in file.read().splitlines()]
        )

    while initial_state.ndim < num_dims:  # Add dims until we reach the target
        initial_state = initial_state[..., None]

    # Part one
    state = initial_state
    for cycle in range(6):

        # Expand the state
        state = np.pad(state, pad_width=[(1, 1)] * state.ndim, constant_values=False)

        def update_cube(coords: Tuple[int, ...]) -> bool:
            patch = state
            for dim in range(state.ndim):
                patch = patch.take(
                    range(
                        max(0, coords[dim] - 1), min(state.shape[dim], coords[dim] + 2)
                    ),
                    axis=dim,
                )
            num_active_neighbours = patch.sum() - state[coords]
            if num_active_neighbours == 3:
                is_cube_active = True
            elif state[coords] and num_active_neighbours == 2:
                is_cube_active = True
            else:
                is_cube_active = False
            return is_cube_active

        # Update the state
        state = np.array([update_cube(pos) for pos in np.ndindex(state.shape)]).reshape(
            state.shape
        )

    print(
        f"The number of cubes left in the active state after the sixth cycle is {state.sum()}."
    )


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="AoC 2020 - Day 17: Conway Cubes")
    parser.add_argument(
        "initial_state_path",
        type=Path,
        help="The path to the starting numbers data file to read",
    )
    parser.add_argument("num_dims", type=int, help="The number of pocket dimensions")
    args = parser.parse_args()
    conway_cubes(args.initial_state_path, args.num_dims)
