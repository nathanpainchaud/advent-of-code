from pathlib import Path
from typing import Set

import pandas as pd


def can_be_contained_by(bags_rules: pd.DataFrame, color: str) -> Set[str]:
    parents = bags_rules[bags_rules.child == color].parent.to_list()
    for parent in parents:
        parents.extend(can_be_contained_by(bags_rules, parent))
    return set(parents)


def number_of_child_bags(bags_rules: pd.DataFrame, color: str) -> int:
    childs = bags_rules[bags_rules.parent == color]
    num_childs = 0
    for child, child_count in zip(childs.child, childs.num):
        num_childs += child_count * (1 + number_of_child_bags(bags_rules, child))
    return num_childs


def bags_rules(bags_rules_path: Path) -> None:
    with open(bags_rules_path) as file:
        bags_rules_text = file.read().splitlines()

    # Build relational table from rules
    bags_rules = pd.DataFrame(columns=["parent", "child", "num"])
    for bags_rule in bags_rules_text:
        rule_tokens = bags_rule.split()
        parent, child_tokens = " ".join(rule_tokens[:2]), rule_tokens[4:]
        if child_tokens[0] != "no":  # if the bag can contain other bags
            for child, num in (
                (" ".join(child_tokens[i + 1 : i + 3]), int(child_tokens[i]))
                for i in range(0, len(child_tokens), 4)
            ):
                bags_rules = bags_rules.append(
                    {"parent": parent, "child": child, "num": num},
                    ignore_index=True,
                )

    shiny_gold_bag_parents = can_be_contained_by(bags_rules, "shiny gold")
    print(
        f"{len(shiny_gold_bag_parents)} bag colors can eventually contain at least one shiny gold bag."
    )

    child_bags = number_of_child_bags(bags_rules, "shiny gold")
    print(
        f"{child_bags} individual bags are required inside your single shiny gold bag."
    )


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="AoC 2020 - Day 7: Handy Haversacks")
    parser.add_argument(
        "bags_rules_path",
        type=Path,
        help="The path to the bags' rules data file to read",
    )
    args = parser.parse_args()
    bags_rules(args.bags_rules_path)
