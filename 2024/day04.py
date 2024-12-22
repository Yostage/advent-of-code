import functools
import re
from dataclasses import dataclass, field
from functools import cache
from typing import Any, Deque, Dict, List, Set, Tuple, TypeVar

from CharacterGrid import CharacterGrid, Directions
from util import Point2D, tuple2_add, tuple2_scalar_mul


def parse_lines(lines: List[str]) -> Any:
    # return None
    return CharacterGrid.from_lines(lines)


def count_xmases(s: str) -> int:
    pat = r"(?=(XMAS|SAMX))"
    this_count = len(re.findall(pat, s))
    if this_count > 0:
        print(f"""{this_count} in [{s}]""")
    return this_count


def get_vector_row(
    initial: Tuple[int, int], direction: Tuple[int, int], map: CharacterGrid
) -> str:
    j = 0
    s = ""
    cursor = initial
    while cursor in map.map:
        s += map.map[cursor]
        cursor = tuple2_add(cursor, direction)
        j += 1
    return s


def part_one(lines) -> int:
    map = parse_lines(lines)
    total = 0

    for x in range(0, map.width()):
        row = get_vector_row((x, 0), Directions.DOWN, map)
        total += count_xmases(row)

    for y in range(0, map.height()):
        row = get_vector_row((0, y), Directions.RIGHT, map)
        total += count_xmases(row)

    # return total
    # diagonals, going south-east
    for x in range(0, map.width()):
        row = get_vector_row((x, 0), (1, 1), map)
        total += count_xmases(row)
    for y in range(1, map.height()):
        row = get_vector_row((0, y), (1, 1), map)
        total += count_xmases(row)

    # diagonals, going south-west
    for x in range(0, map.width()):
        row = get_vector_row((x, 0), (-1, 1), map)
        total += count_xmases(row)
    for y in range(1, map.height()):
        row = get_vector_row((map.max_x(), y), (-1, 1), map)
        total += count_xmases(row)

    print
    return total


def is_xmas(p: Point2D, map: CharacterGrid) -> bool:

    if list(
        sorted(
            [
                c
                for c in [map.map.get(tuple2_add(p, d)) for d in [(-1, -1), (1, 1)]]
                if c is not None
            ]
        )
    ) != ["M", "S"]:
        return False
    if list(
        sorted(
            [
                c
                for c in [map.map.get(tuple2_add(p, d)) for d in [(1, -1), (-1, 1)]]
                if c is not None
            ]
        )
    ) != ["M", "S"]:
        return False

    if map.map[p] != "A":
        return False
    return True


def part_two(lines) -> int:
    map = parse_lines(lines)
    return sum(is_xmas(pt, map) for pt in map.map.keys())


def main() -> None:
    with open("day04_input.txt", "r") as file:
        lines = file.read().splitlines()
        print(part_one(lines))
        print(part_two(lines))


if __name__ == "__main__":
    main()
