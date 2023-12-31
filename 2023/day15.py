import functools
import re
from dataclasses import dataclass, field
from functools import cache
from typing import Any, Dict, List, TypeVar


def parse_lines(lines: List[str]) -> List[str]:
    return lines[0].split(",")


def hash_1(token: str) -> int:
    acc = 0
    for c in token:
        acc += ord(c)
        acc *= 17
        acc %= 256
    return acc


def part_one(lines) -> int:
    tokens = parse_lines(lines)
    return sum(hash_1(token) for token in tokens)


def part_two(lines) -> int:
    parse_lines(lines)
    return 0


def main() -> None:
    with open("day15_input.txt", "r") as file:
        lines = file.read().splitlines()
        print(part_one(lines))
        print(part_two(lines))


if __name__ == "__main__":
    main()
