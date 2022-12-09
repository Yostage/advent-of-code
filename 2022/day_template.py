from functools import cache
import functools
import re
from typing import Any, Dict, List


from dataclasses import dataclass, field
from typing import TypeVar


def parse_lines(lines: List[str]) -> Any:
    return None


def part_one(lines):
    parse_lines(lines)
    return None


def part_two(lines):
    parse_lines(lines)
    return None


def main():
    with open("day9_input.txt", "r") as file:
        lines = file.read().splitlines()
        print(part_one(lines))
        print(part_two(lines))


if __name__ == "__main__":
    main()
