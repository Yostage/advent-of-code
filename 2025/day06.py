import enum
import functools
import re
from collections import defaultdict
from dataclasses import dataclass, field
from functools import cache
from typing import Any, Deque, Dict, List, Set, Tuple, TypeVar


def parse_lines(lines: List[str]) -> Any:
    return lines


def part_one(lines) -> int:
    parse_lines(lines)
    total = 0
    cols = defaultdict(Deque)
    for line in lines:
        for i, c in enumerate(line.split()):
            cols[i].append(c)

    for col in cols.values():
        op = col.pop()
        column_total = int(col.popleft())
        while col:
            val = col.popleft()
            if op == "*":
                column_total *= int(val)
            elif op == "+":
                column_total += int(val)
        total += column_total

    return total


def part_two(lines) -> int:
    parse_lines(lines)
    total = 0
    return total


def main() -> None:
    with open("day06_input.txt", "r") as file:
        lines = file.read().splitlines()
        print(part_one(lines))
        print(part_two(lines))


if __name__ == "__main__":
    main()
