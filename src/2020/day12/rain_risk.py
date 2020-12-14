from pathlib import Path
from typing import Sequence, Tuple

directions = {"N": 1j, "S": -1j, "E": 1, "W": -1}
rotations = {"R": -1j, "L": 1j}


def navigate_ship(
    navigation_instructions: Sequence[Tuple[str, int]]
) -> Tuple[int, int]:
    pos = 0 + 0j
    direction = 1
    for action, value in navigation_instructions:
        if action in directions:
            pos += directions[action] * value
        elif action in rotations:
            direction *= rotations[action] ** (value // 90)
        elif action == "F":
            pos += direction * value
        else:
            raise RuntimeError(f"Invalid action '{action}' encountered.")
    return int(pos.real), int(pos.imag)


def navigate_ship_with_waypoint(
    navigation_instructions: Sequence[Tuple[str, int]]
) -> Tuple[int, int]:
    pos = 0 + 0j
    waypoint = 10 + 1j
    for action, value in navigation_instructions:
        if action in directions:
            waypoint += directions[action] * value
        elif action in rotations:
            waypoint *= rotations[action] ** (value // 90)
        elif action == "F":
            pos += waypoint * value
        else:
            raise RuntimeError(f"Invalid action '{action}' encountered.")
    return int(pos.real), int(pos.imag)


def rain_risk(navigation_instructions_path: Path, use_waypoint: bool) -> None:
    with open(navigation_instructions_path) as file:
        navigation_instructions = [
            (line[0], int(line[1:])) for line in file.read().splitlines()
        ]

    if use_waypoint:
        pos = navigate_ship_with_waypoint(navigation_instructions)
    else:
        pos = navigate_ship(navigation_instructions)
    print(
        "The Manhattan distance between the end location and the ship's starting position is "
        f"{sum(abs(axis) for axis in pos)}."
    )


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="AoC 2020 - Day 12: Rain Risk")
    parser.add_argument(
        "navigation_instructions_path",
        type=Path,
        help="The path to the navigation instructions file to read",
    )
    parser.add_argument(
        "--use_waypoint",
        action="store_true",
        help="Whether the instructions need to be interpreted relative to a waypoint",
    )
    args = parser.parse_args()
    rain_risk(args.navigation_instructions_path, args.use_waypoint)
