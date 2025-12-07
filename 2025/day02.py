import functools
import re
from dataclasses import dataclass, field
from functools import cache
from typing import Any, Deque, Dict, List, Set, Tuple, TypeVar


def parse_lines(lines: List[str]) -> Any:
    return lines[0].split(",")


def part_one(lines) -> int:
    total = 0
    lines = parse_lines(lines)
    for line in lines:
        (min, max) = line.split("-")
        for id in range(int(min), int(max) + 1):
            testable = str(id)
            if len(testable) % 2 != 0:
                continue
            (l, r) = (
                testable[: len(testable) // 2],
                testable[(len(testable) // 2) + len(testable) % 2 :],
            )
            if l == r:
                total += id
                print(f"Found double: {id}")
            # else:
            #     print(f"No double: {id}")

    return total


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
