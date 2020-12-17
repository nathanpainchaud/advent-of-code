from pathlib import Path

import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import maximum_bipartite_matching


def ticket_translation(ticket_notes_path: Path) -> None:

    fields = {}
    tickets = []

    with open(ticket_notes_path) as file:
        notes_block = 0
        lines = file.read().splitlines()
        line_idx = 0
        while line_idx < len(lines):
            if not (line := lines[line_idx]):
                notes_block += 1  # Change the algorithm for interpreting the input
                line_idx += 2  # Skip the first line (the header) of the new block
                continue

            if notes_block == 0:
                field_name, conditions = line.split(":")
                range1, range2 = list(
                    map(
                        lambda x: range(int(x.split("-")[0]), int(x.split("-")[1]) + 1),
                        conditions.replace(" ", "").split("or"),
                    )
                )
                fields[field_name] = range1, range2
            else:
                tickets.append(list(map(int, line.split(","))))

            line_idx += 1

    # Part one
    invalid_values = [
        (ticket_id, val)
        for ticket_id, vals in enumerate(tickets)
        for val in vals
        if not any(val in range1 or val in range2 for range1, range2 in fields.values())
    ]

    print(
        f"The ticket scanning error rate is {sum(invalid_val for _, invalid_val in invalid_values)}."
    )

    # Part two
    invalid_tickets = sorted(set(ticket_id for ticket_id, _ in invalid_values))
    tickets = np.array(
        [ticket for id, ticket in enumerate(tickets) if id not in invalid_tickets]
    )

    field_validity_matrix = [
        [
            all(val in range1 or val in range2 for val in tickets[:, field_rank])
            for field_name, (range1, range2) in fields.items()
        ]
        for field_rank in range(len(fields))
    ]
    bipartite_matching = maximum_bipartite_matching(csr_matrix(field_validity_matrix))
    field_ranks = {
        field_name: bipartite_matching[idx]
        for idx, field_name in enumerate(fields.keys())
    }

    product = np.prod(
        [
            tickets[0, field_rank]
            for field_name, field_rank in field_ranks.items()
            if field_name.startswith("departure")
        ]
    )
    print(
        f"The product of the six fields on the ticket that start with the word departure is {product}."
    )


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="AoC 2020 - Day 16: Ticket Translation"
    )
    parser.add_argument(
        "ticket_notes_path",
        type=Path,
        help="The path to the notes about the ticket fields to read",
    )
    args = parser.parse_args()
    ticket_translation(args.ticket_notes_path)
