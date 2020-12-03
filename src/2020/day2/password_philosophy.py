from pathlib import Path
from typing import Callable


def is_password_sled_valid(first: int, second: int, letter: str, password: str) -> bool:
    return first <= password.count(letter) <= second


def is_password_tobogan_valid(
    first: int, second: int, letter: str, password: str
) -> bool:
    return (password[first - 1] == letter) ^ (password[second - 1] == letter)


def validate_passwords(
    passwords_path: Path, is_password_valid_fn: Callable[[int, int, str, str], bool]
) -> None:
    with open(passwords_path) as file:
        passwords_w_policy = file.read().splitlines()
    valid_passwords = []
    for password_w_policy in passwords_w_policy:
        first, second, letter, password = (
            password_w_policy.replace("-", " ").replace(":", " ").split()
        )
        if is_password_valid_fn(int(first), int(second), letter, password):
            valid_passwords.append(password_w_policy)
    print(f"{len(valid_passwords)} valid passwords were found: ")
    print("\n".join(valid_passwords))


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="AoC 2020 - Day 2: Password Philosophy"
    )
    parser.add_argument(
        "passwords_path", type=Path, help="The path to the passwords file to read"
    )
    parser.add_argument(
        "password_policy",
        type=str,
        choices=["sled", "tobogan"],
        help="The policy to use to determine if the password is valid",
    )
    args = parser.parse_args()
    validate_passwords(
        args.passwords_path, locals()[f"is_password_{args.password_policy}_valid"]
    )
