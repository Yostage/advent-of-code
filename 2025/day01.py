import functools
import re
from dataclasses import dataclass, field
from functools import cache
from typing import Any, Deque, Dict, List, Set, Tuple, TypeVar


def parse_lines(lines: List[str]) -> Any:
    return [(line[0], int(line[1:])) for line in lines]


def part_one(lines) -> int:
    dial = 50
    clicks = 0
    turns = parse_lines(lines)
    for turn in turns:
        direction, distance = turn
        if direction == "L":
            dial -= distance
        else:
            dial += distance
        dial %= 100
        if dial == 0:
            clicks += 1

    return clicks


def part_two(lines) -> int:
    parse_lines(lines)
    return 0


def main() -> None:
    with open("day01_input.txt", "r") as file:
        lines = file.read().splitlines()
        print(part_one(lines))
        print(part_two(lines))


if __name__ == "__main__":
    main()
