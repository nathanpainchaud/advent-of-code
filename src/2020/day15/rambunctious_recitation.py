from pathlib import Path


def rambunctious_recitation(starting_numbers_path: Path, num_turns: int) -> None:

    with open(starting_numbers_path) as file:
        starting_numbers = [int(number) for number in file.read().split(",")]

    numbers = {number: turn for turn, number in enumerate(starting_numbers[:-1], 1)}
    last_number, number = starting_numbers[-1], starting_numbers[-1]
    for turn in range(len(starting_numbers) + 1, num_turns + 1):
        number = turn - 1 - numbers.get(last_number, 0)
        numbers[last_number] = turn - 1  # Mark turn of last number
        if number == turn - 1:  # If the number had never been said before
            number = 0
        last_number = number

    print(f"The {num_turns}th number spoken will be {number}.")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="AoC 2020 - Day 15: Rambunctious Recitation"
    )
    parser.add_argument(
        "starting_numbers_path",
        type=Path,
        help="The path to the starting numbers data file to read",
    )
    parser.add_argument("num_turns", type=int, help="Number of turns to play the game")
    args = parser.parse_args()
    rambunctious_recitation(args.starting_numbers_path, args.num_turns)
