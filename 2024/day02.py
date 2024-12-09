import functools
import re
from dataclasses import dataclass, field
from functools import cache
from itertools import islice, tee
from typing import Any, Deque, Dict, List, Set, Tuple, TypeVar

from util import sgn


def parse_lines(lines: List[str]) -> Any:
    # return [[int(x) for x in line in lines for x in line]
    return [[int(x) for x in line.split(" ")] for line in lines]


def pairwise_with_repetition(iterable):
    # Create two iterators from the input iterable
    a, b = tee(iterable)
    # Advance the second iterator by one
    b = islice(b, 1, None)
    # Zip the two iterators together
    return zip(a, b)


def report_is_safe(report: List[int]):
    dir = sgn(report[1] - report[0])
    if dir == 0:
        return False
    for pair in pairwise_with_repetition(report):
        delta = pair[1] - pair[0]

        if sgn(delta) != dir:
            return False

        if abs(delta) > 3:
            return False
    print(f"{report}: true")
    return True


def part_one(lines) -> int:
    reports = parse_lines(lines)
    return sum(1 if report_is_safe(report) else 0 for report in reports)


def part_two(lines) -> int:
    parse_lines(lines)
    return 0


def main() -> None:
    with open("day02_input.txt", "r") as file:
        lines = file.read().splitlines()
        print(part_one(lines))
        print(part_two(lines))


if __name__ == "__main__":
    main()
