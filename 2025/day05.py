import functools
import re
from dataclasses import dataclass, field
from functools import cache
from typing import Any, Deque, Dict, List, Set, Tuple, TypeVar


def parse_lines(lines: List[str]) -> Any:
    i = iter(lines)
    ranges = []
    for line in i:
        if "-" not in line:
            break
        ranges.append(tuple(map(int, line.split("-"))))

    # next(i)

    ingredients = []
    for line in i:
        ingredients.append(int(line))

    assert len(ranges) > 0
    assert len(ingredients) > 0
    return (ranges, ingredients)


def part_one(lines) -> int:
    def test_ranges(ranges, i):
        return any(r[0] <= i <= r[1] for r in ranges)

    (ranges, ingredients) = parse_lines(lines)
    return sum(1 if test_ranges(ranges, i) else 0 for i in ingredients)


def part_two(lines) -> int:
    # sort intervals and merge overlapping ones
    # then just sum them all
    ranges, _ = parse_lines(lines)
    ranges = list(sorted(ranges, key=lambda x: x[0]))
    merged = []
    for r in ranges:
        if not merged or merged[-1][1] < r[0] - 1:
            merged.append(r)
        else:
            merged[-1] = (merged[-1][0], max(merged[-1][1], r[1]))
    return sum(r[1] - r[0] + 1 for r in merged)


def main() -> None:
    with open("day05_input.txt", "r") as file:
        lines = file.read().splitlines()
        print(part_one(lines))
        print(part_two(lines))


if __name__ == "__main__":
    main()
