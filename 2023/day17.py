import functools
import re
from dataclasses import dataclass, field
from functools import cache
from typing import Any, Dict, List, TypeVar

from CharacterGrid import CharacterGrid


def parse_lines(lines: List[str]) -> CharacterGrid:
    return CharacterGrid.from_lines(lines)


def part_one(lines) -> int:
    grid = parse_lines(lines)
    return 0


def part_two(lines) -> int:
    parse_lines(lines)
    return 0


def main() -> None:
    with open("day17_input.txt", "r") as file:
        lines = file.read().splitlines()
        print(part_one(lines))
        print(part_two(lines))


if __name__ == "__main__":
    main()
