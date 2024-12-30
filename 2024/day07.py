import functools
import re
from dataclasses import dataclass, field
from functools import cache
from typing import Any, Deque, Dict, List, Set, Tuple, TypeVar


def parse_lines(lines: List[str]) -> Any:
    equations = []
    for line in lines:
        (l, r) = line.split(": ")
        values = [float(v) for v in r.split(" ")]
        equations.append((l, values))
    return equations


def can_equation_make_value(value: float, operands: List[float]) -> bool:
    # base case
    if len(operands) == 1:
        return value == operands[0]

    # try addition
    # try multiplication
    last_operand = operands[-1]
    return can_equation_make_value(
        value - last_operand, operands[0:-1]
    ) or can_equation_make_value(value / last_operand, operands[0:-1])


def part_one(lines) -> int:
    equations = parse_lines(lines)
    return sum(
        int(total)
        for (total, operands) in equations
        if can_equation_make_value(float(total), operands)
    )


def part_two(lines) -> int:
    parse_lines(lines)
    return 0


def main() -> None:
    with open("day07_input.txt", "r") as file:
        lines = file.read().splitlines()
        print(part_one(lines))
        print(part_two(lines))


if __name__ == "__main__":
    main()
