from functools import reduce
from operator import mul
from pathlib import Path


def tobogan_trajectory(map_path: Path, slopes_path: Path) -> None:
    with open(map_path) as file:
        area_map = file.read().splitlines()

    with open(slopes_path) as file:
        slopes = [tuple(map(int, line.split())) for line in file.read().splitlines()]

    horizontal_pattern_len = len(area_map[0])
    nb_trees_hit_wrt_slope = []
    for slope in slopes:
        horizontal_slope, vertical_slope = slope
        horizontal_pos, vertical_pos = 0, 0
        nb_trees_hit = 0
        while vertical_pos < len(area_map):
            # Detect if we hit a treefollowing
            nb_trees_hit += (
                area_map[vertical_pos][horizontal_pos % horizontal_pattern_len] == "#"
            )

            # Move following the slope
            vertical_pos += vertical_slope
            horizontal_pos += horizontal_slope

        nb_trees_hit_wrt_slope.append(nb_trees_hit)
        print(
            f"We hit {nb_trees_hit} trees while following a slope of "
            f"right {horizontal_slope} and down {vertical_slope}."
        )

    print(
        f"Product of the number of trees hit w.r.t. each slope: {reduce(mul, nb_trees_hit_wrt_slope)}"
    )


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="AoC 2020 - Day 3: Tobogan Trajectory")
    parser.add_argument(
        "map_path", type=Path, help="The path to the area map file to read"
    )
    parser.add_argument(
        "slopes_path",
        type=Path,
        help="The path to the file describing the slopes to read",
    )
    args = parser.parse_args()
    tobogan_trajectory(args.map_path, args.slopes_path)
