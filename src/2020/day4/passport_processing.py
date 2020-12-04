import re
import string
import sys
from pathlib import Path
from typing import Any, Callable, Dict


def has_passport_required_fields(passport: Dict[str, Any]) -> bool:
    passport_copy = passport.copy()
    passport_copy.pop("cid", None)
    return len(passport_copy) == 7


def is_byr_valid(val: str) -> bool:
    return 1920 <= int(val) <= 2002


def is_iyr_valid(val: str) -> bool:
    return 2010 <= int(val) <= 2020


def is_eyr_valid(val: str) -> bool:
    return 2020 <= int(val) <= 2030


def is_hgt_valid(val: str) -> bool:
    try:
        height_val, height_unit = int(val[:-2]), val[-2:]
    except ValueError:
        return False
    return (
        150 <= height_val <= 193
        if height_unit == "cm"
        else 59 <= height_val <= 76
        if height_unit == "in"
        else False
    )


def is_hcl_valid(val: str) -> bool:
    return val[0] == "#" and all(c in string.hexdigits for c in val[1:])


def is_ecl_valid(val: str) -> bool:
    return val in ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]


def is_pid_valid(val: str) -> bool:
    return bool(re.compile("^[0-9]{9}$").match(val))


def is_passport_valid(passport: Dict[str, Any]) -> bool:
    if has_passport_required_fields(passport):
        are_fields_valid = all(
            getattr(sys.modules[__name__], f"is_{field}_valid")(val)
            for field, val in passport.items()
            if field != "cid"
        )
        return are_fields_valid
    return False


def passport_processing(
    passports_path: Path, is_passport_valid_fn: Callable[[Dict[str, Any]], bool]
) -> None:
    with open(passports_path) as file:
        passports_lines = file.read().splitlines()

    # Group data by passport
    passports = [{}]
    for line in passports_lines:
        if not line:  # Create a new entry for a passport on a blank line
            passports.append({})
            continue

        passport = passports[-1]

        # Build dict of the current line's data, and add it to the current passport
        passport_data_list = re.split("[: ]", line)
        data_keys = passport_data_list[0::2]
        data_values = passport_data_list[1::2]
        passport.update(dict(zip(data_keys, data_values)))

    num_valid_passports = sum(is_passport_valid_fn(passport) for passport in passports)

    print(f"The batch contains {num_valid_passports} valid passports.")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="AoC 2020 - Day 4: Passport Processing"
    )
    parser.add_argument(
        "passports_path", type=Path, help="The path to the passports data file to read"
    )
    parser.add_argument("validation", type=str, choices=["present", "valid"])
    args = parser.parse_args()
    if args.validation == "present":
        is_passport_valid_fn = has_passport_required_fields
    else:  # args.validation == "valid"
        is_passport_valid_fn = is_passport_valid
    passport_processing(args.passports_path, is_passport_valid_fn)
