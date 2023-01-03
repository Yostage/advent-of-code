import functools
import re
from dataclasses import dataclass, field
from functools import cache
from typing import Any, Dict, List, TypeVar

SnafuEncoded = str


int_to_snafu_encodings = {
    2: "2",
    1: "1",
    0: "0",
    -1: "-",
    -2: "=",
}

snafu_to_int_encodings = {v: k for k, v in int_to_snafu_encodings.items()}


def int_to_snafu(input: int) -> SnafuEncoded:
    if input == 0:
        return "0"
    base = 5
    encodings = {
        2: "2",
        1: "1",
        0: "0",
        -1: "-",
        -2: "=",
    }
    enc = [0, 1, 2, -2, -1]
    total = input
    place = 0
    output = []
    while total != 0 and place < 10000:
        this_digit = (total // (base**place)) % (base)
        # but, surprise, we can't actually write the digit we wanted
        output.append(encodings[enc[this_digit]])
        # so handle that we wrote the digit we had instead and keep going
        total -= enc[this_digit] * (base**place)
        place += 1

    return "".join(reversed(output))


def snafu_to_int(input: str) -> int:
    base = 5
    return sum(
        snafu_to_int_encodings[digit] * (base**idx)
        for idx, digit in enumerate(reversed(list(input)))
    )


def parse_lines(lines: List[str]) -> List[str]:
    return lines


def part_one(lines) -> str:
    snafus = parse_lines(lines)
    total = sum(snafu_to_int(s) for s in snafus)
    return int_to_snafu(total)
    # for x in range(20):
    #     print(f"{x} => {int_to_snafu(x)} => {snafu_to_int(int_to_snafu(x))}")
    # return 0


def main() -> None:
    with open("day25_input.txt", "r") as file:
        lines = file.read().splitlines()
        print(part_one(lines))


if __name__ == "__main__":
    main()
