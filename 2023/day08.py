import functools
import re
from dataclasses import dataclass, field
from functools import cache
from itertools import cycle
from typing import Any, Dict, List, TypeVar


def parse_lines(lines: List[str]) -> Any:
    instructions = [c for c in lines[0]]
    lefts: Dict[str, str] = {}
    rights: Dict[str, str] = {}
    for line in lines[2:]:
        node, rest = line.split(" = ")
        (left, right) = rest[1:-1].split(", ")
        lefts[node] = left
        rights[node] = right

    return (instructions, {"L": lefts, "R": rights})


def part_one(lines) -> int:
    (instructions, nested_map) = parse_lines(lines)
    current_node = "AAA"
    for idx, step in enumerate(cycle(instructions)):
        current_node = nested_map[step][current_node]
        if current_node == "ZZZ":
            return idx + 1
    assert False


def part_two(lines) -> int:
    parse_lines(lines)
    return 0


def main() -> None:
    with open("day08_input.txt", "r") as file:
        lines = file.read().splitlines()
        print(part_one(lines))
        print(part_two(lines))


if __name__ == "__main__":
    main()
