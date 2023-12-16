import functools
import re
from dataclasses import dataclass, field
from functools import cache
from typing import Any, Dict, List, TypeVar

from util import Point2D


def parse_lines(lines: List[str]) -> List[Point2D]:
    return [
        (x, y) for y, line in enumerate(lines) for x, c in enumerate(line) if c == "#"
    ]


def part_one(lines) -> int:
    galaxies = parse_lines(lines)
    return 0


def part_two(lines) -> int:
    parse_lines(lines)
    return 0


def main() -> None:
    with open("day11_input.txt", "r") as file:
        lines = file.read().splitlines()
        print(part_one(lines))
        print(part_two(lines))


if __name__ == "__main__":
    main()
