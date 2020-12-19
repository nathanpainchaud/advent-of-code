import functools
import itertools
import re
from pathlib import Path
from typing import Dict, List, Sequence, Union


def list_matching_messages(
    rules: Dict[int, Union[str, List[str]]], rule_id: int
) -> Sequence[str]:
    if isinstance(
        rules[rule_id], list
    ):  # If we've already computed the matches for the rule
        rule_matches = rules[rule_id]

    else:  # Compute the rule's matches
        rule = rules[rule_id]
        if match := re.search(r"\"(.)\"", rule):  # If the rule is a single character
            rule_matches = [match.group(1)]

        else:  # If the rule is a mixture of other rules
            rule_matches = []
            for subrule in rule.split("|"):
                rule_matches.extend(
                    functools.reduce(
                        lambda prefixes, next_rule_id: [
                            prefix + next_rule_match
                            for prefix, next_rule_match in itertools.product(
                                prefixes, list_matching_messages(rules, next_rule_id)
                            )
                        ],
                        map(int, subrule.split()),
                        [""],
                    )
                )

        rules[rule_id] = rule_matches

    return rule_matches


def monster_messages(messages_path: Path) -> None:

    with open(messages_path) as file:
        lines = file.read().splitlines()
        sep_line = lines.index("")
        rules = {
            int(line.split(":")[0]): line.split(":")[1] for line in lines[:sep_line]
        }
        messages = lines[sep_line + 1 :]

    rule0_matches = list_matching_messages(rules, 0)
    matching_messages = [message for message in messages if message in rule0_matches]
    print(
        f"The number of messages that completely match rule 0 is {len(matching_messages)}."
    )


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="AoC 2020 - Day 19: Monster Messages")
    parser.add_argument(
        "messages_path",
        type=Path,
        help="The path to the messages and rules file to read",
    )
    args = parser.parse_args()
    monster_messages(args.messages_path)
