import string
from pathlib import Path
from typing import Literal


def custom_customs(
    groups_answers_path: Path, answer_condition: Literal["anyone", "everyone"]
) -> None:
    with open(groups_answers_path) as file:
        groups_answers_lines = file.read().splitlines()

    if answer_condition == "anyone":
        group_answer_update_fn = "union"
        init_group_answers = set
    else:  # answer_condition == "everyone"
        group_answer_update_fn = "intersection"
        init_group_answers = lambda: set(string.ascii_lowercase[:26])

    # Group answers by groups
    groups_answers = [init_group_answers()]
    for line in groups_answers_lines:
        if not line:  # Create a set of answers for a group on a blank line
            groups_answers.append(init_group_answers())
            continue

        group_answers = groups_answers[-1]
        # group_answers.update(line)
        groups_answers[-1] = getattr(group_answers, group_answer_update_fn)(line)

    print(
        f"Over all groups, {answer_condition} answered 'yes' to {sum(len(group_answers) for group_answers in groups_answers)} questions."
    )


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="AoC 2020 - Day 6: Custom Customs")
    parser.add_argument(
        "groups_answers_path",
        type=Path,
        help="The path to the groups' answers data file to read",
    )
    parser.add_argument(
        "answer_condition",
        type=str,
        choices=["anyone", "everyone"],
        help="The condition to count 'yes' answers from a group",
    )
    args = parser.parse_args()
    custom_customs(args.groups_answers_path, args.answer_condition)
