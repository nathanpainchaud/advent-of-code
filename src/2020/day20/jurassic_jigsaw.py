from pathlib import Path

import numpy as np


def jurassic_jigsaw(tiles_path: Path) -> None:

    with open(tiles_path) as file:
        tiles = {}
        lines = file.read().splitlines()
        tile_ends = [idx for idx, line in enumerate(lines) if not line]
        tile_begins = [0] + [tile_end + 1 for tile_end in tile_ends[:-1]]
        for tile_begin, tile_end in zip(tile_begins, tile_ends):
            tile_idx = int(lines[tile_begin][:-1].split()[-1])
            tiles[tile_idx] = np.array(
                [list(line) for line in lines[tile_begin + 1 : tile_end]]
            )

    print(f"The product of the IDs of the four corner tiles is .")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="AoC 2020 - Day 20: Jurassic Jigsaw")
    parser.add_argument(
        "tiles_path",
        type=Path,
        help="The path to the tiles data file to read",
    )
    args = parser.parse_args()
    jurassic_jigsaw(args.tiles_path)
