import itertools
from pathlib import Path
from typing import Literal, Mapping, Sequence, Tuple, Union

MaskOp = Tuple[Literal["mask"], str]
MemOp = Tuple[Literal["mem"], str, str]
Op = Union[MaskOp, MemOp]
Program = Sequence[Op]
Memory = Mapping[int, int]


def decoder_v1(mask: str, address: str, val: str) -> Memory:
    val = "".join(
        mask[bit_rank] if is_masked else val[bit_rank]
        for bit_rank, is_masked in enumerate(bit != "X" for bit in mask)
    )
    return {int(address, 2): int(val, 2)}


def decoder_v2(mask: str, address: str, val: str) -> Memory:
    val = int(val, 2)
    floating_address = "".join(
        address[bit_rank] if mask_bit == "0" else mask[bit_rank]
        for bit_rank, mask_bit in enumerate(mask)
    )
    floating_bits = [
        bit_rank for bit_rank, bit in enumerate(floating_address) if bit == "X"
    ]
    memory = {}
    for bit_vals in itertools.product(("0", "1"), repeat=len(floating_bits)):
        address_bits = list(floating_address)
        for floating_bit, bit_val in zip(floating_bits, bit_vals):
            address_bits[floating_bit] = bit_val
        memory["".join(address_bits)] = val
    return memory


def run_program(initialization_program: Program, decoder_version: str) -> Memory:
    memory = {}
    for op in initialization_program:
        op_t, *args = op
        if op_t == "mask":
            mask = args[0]
        elif op_t == "mem":
            address, val = args
            memory.update(globals()[f"decoder_{decoder_version}"](mask, address, val))
        else:
            raise RuntimeError(
                f"Unknown '{op_t}' operation called with parameters: {args}."
            )
    return memory


def docking_data(initialization_program_path: Path, decoder_version: str) -> None:
    def binary_str_36(val: int) -> str:
        return bin(val)[2:].zfill(36)

    with open(initialization_program_path) as file:
        initialization_program = []
        for line_nb, line in enumerate(file.read().splitlines()):
            tokens = line.replace("=", " ").replace("[", " ").replace("]", " ").split()
            if len(tokens) == 2:  # MaskOp
                initialization_program.append(tokens)
            elif len(tokens) == 3:  # MemOp
                address = binary_str_36(int(tokens[1]))
                val = binary_str_36(int(tokens[2]))
                initialization_program.append((tokens[0], address, val))
            else:
                raise RuntimeError(
                    f"Unable to parse initialization program line {line_nb}: {line}"
                )

    memory = run_program(initialization_program, decoder_version)
    print(
        f"The sum of all values left in memory after the program completes is {sum(memory.values())}."
    )


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="AoC 2020 - Day 14: Docking Data")
    parser.add_argument(
        "initialization_program_path",
        type=Path,
        help="The path to the initialization program to read",
    )
    parser.add_argument(
        "decoder_version",
        type=str,
        choices=["v1", "v2"],
        help="The version of the decoder chip to emulate",
    )
    args = parser.parse_args()
    docking_data(args.initialization_program_path, args.decoder_version)
