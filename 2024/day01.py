import functools
import re
from collections import Counter
from dataclasses import dataclass, field
from functools import cache
from typing import Any, Deque, Dict, List, Set, Tuple, TypeVar


def parse_lines(lines: List[str]) -> Any:
    return [line.split() for line in lines]


def part_one(lines) -> int:
    v = parse_lines(lines)
    left, right = zip(*v)
    deltas = [abs(int(r) - int(l)) for (l, r) in zip(sorted(left), sorted(right))]
    return sum(deltas)


def part_two(lines) -> int:
    v = parse_lines(lines)
    left, right = zip(*v)
    frequencies = Counter(right)
    similarities = [int(x) * frequencies.get(x, 0) for x in left]
    return sum(similarities)


def main() -> None:
    with open("day01_input.txt", "r") as file:
        lines = file.read().splitlines()
        print(part_one(lines))
        print(part_two(lines))


if __name__ == "__main__":
    main()
