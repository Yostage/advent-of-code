import functools
import itertools
import re
from dataclasses import dataclass, field
from functools import cache

from CharacterGrid import CharacterGrid


def parse_lines(lines: list[str]) -> CharacterGrid:
    reds = [(int(a), int(b)) for line in lines for a, b in [line.split(",")]]
    # reds = [tuple(map(int, line.split(","))) for line in lines]
    grid = CharacterGrid({})
    for r in reds:
        grid.map[r] = "#"

    return grid


def part_one(lines) -> int:
    grid = parse_lines(lines)
    all_reds = [k for k, v in grid.map.items() if v == "#"]
    print(all_reds)
    total = 0
    for pair in itertools.combinations(all_reds, 2):
        total = max(
            total,
            (abs(pair[0][0] - pair[1][0]) + 1) * (abs(pair[0][1] - pair[1][1]) + 1),
        )
    return total


def part_two(lines) -> int:
    grid = parse_lines(lines)
    # maybe: sort all the rectangles by size in a max_heap and then test them, top down
    # maybe the green tiles can be stored as rectangles themselves
    total = 0
    return total


def main() -> None:
    with open("day09_input.txt", "r") as file:
        lines = file.read().splitlines()
        print(part_one(lines))
        print(part_two(lines))


if __name__ == "__main__":
    main()
    main()
