import functools
import re
from dataclasses import dataclass, field
from functools import cache
from typing import Any, Deque, Dict, List, Set, Tuple, TypeVar

from CharacterGrid import CharacterGrid, all_adjacencies
from util import Point2D, tuple2_add


def parse_lines(lines: List[str]) -> CharacterGrid:
    return CharacterGrid.from_lines(lines)


def part_one(lines) -> int:
    grid = parse_lines(lines)
    grid.render()
    total = 0
    candidates = []
    for pt in grid.map.keys():
        # for pt in [(2, 0)]:
        if grid.map[pt] != "@":
            continue
        neighbor_count = 0
        for dir in all_adjacencies:
            neighbor = tuple2_add(pt, dir)
            if neighbor in grid.map and grid.map[neighbor] == "@":
                neighbor_count += 1
                # print(f"  neighbor at {neighbor}")
        # print(f"Point {pt} has {neighbor_count} neighbors")
        if neighbor_count < 4:
            candidates.append(pt)
            total += 1

    for pt in candidates:
        grid.map[pt] = "x"
    grid.render()

    return total


def part_two(lines) -> int:
    parse_lines(lines)
    return 0


def main() -> None:
    with open("day04_input.txt", "r") as file:
        lines = file.read().splitlines()
        print(part_one(lines))
        print(part_two(lines))


if __name__ == "__main__":
    main()
