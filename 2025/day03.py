import functools
import re
from dataclasses import dataclass, field
from functools import cache
from typing import Any, Deque, Dict, List, Set, Tuple, TypeVar


def parse_lines(lines: List[str]) -> Any:
    return lines


def part_one(lines) -> int:
    parse_lines(lines)
    total = 0
    for line in lines:
        batteries = [int(x) for x in line]
        tens_place = max(batteries[:-1])
        first_battery = batteries.index(tens_place)
        the_rest = batteries[first_battery + 1 :]
        ones_place = max(the_rest)
        total += 10 * tens_place + ones_place
    return total


def part_two(lines) -> int:
    parse_lines(lines)
    return 0


def main() -> None:
    with open("day03_input.txt", "r") as file:
        lines = file.read().splitlines()
        print(part_one(lines))
        print(part_two(lines))


if __name__ == "__main__":
    main()
