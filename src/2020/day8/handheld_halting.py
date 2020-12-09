from copy import deepcopy
from pathlib import Path
from typing import Callable, List, Tuple

from tqdm import tqdm

Code = List[Tuple[str, int]]
ExitCode = Tuple[bool, int]


def run_code(code: Code) -> ExitCode:
    next_instruction_idx = 0
    executed_instructions = set()
    acc = 0
    while (
        next_instruction_idx not in executed_instructions
        and next_instruction_idx < len(code)
    ):
        executed_instructions.add(next_instruction_idx)
        op, arg = code[next_instruction_idx]
        if op == "acc":
            acc += arg
        elif op == "jmp":
            next_instruction_idx += arg
            continue
        elif op == "nop":
            pass
        else:
            raise RuntimeError(f"Unknown instruction type: {op}.")
        next_instruction_idx += 1

    return next_instruction_idx == len(code), acc


def edit_instruction(code: Code, target_instruction: int, target_op: str) -> Code:
    code_copy = deepcopy(code)
    code_copy[target_instruction] = (target_op, code[target_instruction][1])
    return code_copy


def repair_code(code: Code) -> ExitCode:
    # Identify instructions that might have been corrupted (any jmp or nop in the code)
    jumps_to_edit = [
        idx for idx, instruction in enumerate(code) if instruction[0] == "jmp"
    ]
    nops_to_edit = [
        idx for idx, instruction in enumerate(code) if instruction[0] == "nop"
    ]
    target_ops = (["nop"] * len(jumps_to_edit)) + (["jmp"] * len(nops_to_edit))

    # Brute force code repair by trying to switch every possibly corrupted instruction
    has_program_terminated_correctly = False
    pbar = tqdm(jumps_to_edit + nops_to_edit, unit="instruction")
    for instruction_to_edit, target_op in zip(pbar, target_ops):
        pbar.set_description(
            f"Running code with instruction {instruction_to_edit} op switched to '{target_op}'"
        )
        has_program_terminated_correctly, acc = run_code(
            edit_instruction(code, instruction_to_edit, target_op)
        )
        if has_program_terminated_correctly:
            break

    if not has_program_terminated_correctly:
        raise RuntimeError(
            "Could not find an instruction to edit that allowed for the program to terminate correctly."
        )
    else:
        return True, acc


def handheld_halting(boot_code_path: Path, run_fn: Callable[[Code], ExitCode]) -> None:
    with open(boot_code_path) as file:
        boot_code_instructions = [
            (line.split()[0], int(line.split()[1])) for line in file.read().splitlines()
        ]

    has_program_terminated_correctly, acc = run_fn(boot_code_instructions)

    if has_program_terminated_correctly:
        msg = "The program terminated correctly, "
    else:
        msg = "The program terminated on an infinite loop, "
    msg += f"with a value of {acc} in the accumulator."
    print(msg)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="AoC 2020 - Day 8: Handheld Halting")
    parser.add_argument(
        "boot_code_path",
        type=Path,
        help="The path to the boot code instructions file to read",
    )
    parser.add_argument("run_mode", type=str, choices=["run", "repair"])
    args = parser.parse_args()
    handheld_halting(args.boot_code_path, globals()[f"{args.run_mode}_code"])
