import functools
import re
from dataclasses import dataclass, field
from functools import cache
from typing import Any, Deque, Dict, List, Set, Tuple, TypeVar


def parse_lines(lines: List[str]) -> Any:
    return lines


def part_one(lines) -> int:
    lines = parse_lines(lines)
    pattern = r"mul\((\d+),(\d+)\)"
    tuples_of_numbers: List[Tuple[int, int]] = []

    for line in lines:
        matches = re.findall(pattern, line)
        tuples_of_numbers.extend((int(match[0]), int(match[1])) for match in matches)

    return sum(x * y for x, y in tuples_of_numbers)


def part_two(lines) -> int:
    lines = parse_lines(lines)
    # pattern = r"(mul|do|don't)(?:\((\d+),(\d+)\))"
    pattern = r"(mul|do|don't)\((\d+)?,?(\d+)?\)"
    tuples_of_operations: List[Tuple[str, int, int]] = []

    for line in lines:
        matches = re.findall(pattern, line)
        tuples_of_operations.extend(
            (
                match[0],
                int(match[1]) if match[1] else 0,
                int(match[2]) if match[2] else 0,
            )
            for match in matches
        )

    print(tuples_of_operations)

    total_sum = 0
    enabled = 1
    for operator, x, y in tuples_of_operations:

        if operator == "mul":
            total_sum += x * y if enabled else 0
        elif operator == "do":
            enabled = 1
        elif operator == "don't":
            enabled = 0

    return total_sum


def main() -> None:
    with open("day03_input.txt", "r") as file:
        lines = file.read().splitlines()
        print(part_one(lines))
        print(part_two(lines))


if __name__ == "__main__":
    main()
