import functools
import re
from dataclasses import dataclass, field
from functools import cache
from typing import Any, Deque, Dict, List, Set, Tuple, TypeVar


def parse_lines(lines: List[str]) -> List[Tuple[str, List[str]]]:
    equations = []
    for line in lines:
        (l, r) = line.split(": ")
        values = [v for v in r.split(" ")]
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
        if can_equation_make_value(float(total), [float(o) for o in operands])
    )


def concat(l: int, r: int) -> int:
    return int(str(l) + str(r))


# @cache
def can_day2_make_value(value: int, lhs: int, operands: Tuple[int, ...]) -> bool:
    # base case
    if len(operands) == 1:
        remaining = operands[0]
        return (
            value == (lhs + remaining)
            or value == (lhs * remaining)
            or value == concat(lhs, remaining)
        )

    popped_op = operands[0]
    return (
        can_day2_make_value(value, lhs + popped_op, operands[1:])
        or can_day2_make_value(value, lhs * popped_op, operands[1:])
        or can_day2_make_value(value, concat(lhs, popped_op), operands[1:])
    )


def part_two(lines) -> int:
    equations = parse_lines(lines)
    return sum(
        int(total)
        for (total, operands) in equations
        if can_day2_make_value(
            int(total), int(operands[0]), tuple([int(o) for o in operands[1:]])
        )
    )


def main() -> None:
    with open("day07_input.txt", "r") as file:
        lines = file.read().splitlines()
        print(part_one(lines))
        print(part_two(lines))


if __name__ == "__main__":
    main()
