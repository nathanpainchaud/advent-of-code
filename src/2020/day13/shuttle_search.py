from pathlib import Path

from sympy.ntheory.modular import solve_congruence


def shuttle_search(notes_path: Path) -> None:
    with open(notes_path) as file:
        lines = [line for line in file.read().splitlines()]
    earliest_timestamp = int(lines[0])
    bus_ids = {
        int(id): rank for rank, id in enumerate(lines[1].split(",")) if id != "x"
    }

    # Part one
    bus_wait_times = {
        bus_id: bus_id - (earliest_timestamp % bus_id) for bus_id in bus_ids
    }
    earliest_bus = min(bus_wait_times, key=bus_wait_times.get)

    print(
        "The ID of the earliest bus we can take to the airport multiplied by the number of minutes we'll need to wait "
        f"for that bus is {earliest_bus * bus_wait_times[earliest_bus]}."
    )

    # Part two
    timestamp = solve_congruence(
        *[(bus_id - rank, bus_id) for bus_id, rank in bus_ids.items()]
    )[0]

    print(
        f"The earliest timestamp such that all of the listed bus IDs depart at offsets matching their positions in the "
        f"list is {timestamp}."
    )


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="AoC 2020 - Day 13: Shuttle Search")
    parser.add_argument(
        "notes_path",
        type=Path,
        help="The path to the notes about the shuttles to read",
    )
    args = parser.parse_args()
    shuttle_search(args.notes_path)
