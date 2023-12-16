import functools
import re
from dataclasses import dataclass, field
from functools import cache
from typing import Any, Dict, List, TypeVar

from util import Point2D, manhattan_distance


def parse_lines(lines: List[str]) -> List[Point2D]:
    return [
        (x, y) for y, line in enumerate(lines) for x, c in enumerate(line) if c == "#"
    ]


def calculate_distances(galaxies: List[Point2D], expand_delta: int) -> int:
    max_y = max(galaxy[1] for galaxy in galaxies)
    max_x = max(galaxy[0] for galaxy in galaxies)
    x_locs = set(galaxy[0] for galaxy in galaxies)
    y_locs = set(galaxy[1] for galaxy in galaxies)
    stretched_columns = [x for x in range(0, max_x + 1) if x not in x_locs]
    stretched_rows = [y for y in range(0, max_y + 1) if y not in y_locs]
    # print(stretched_columns)
    # print(stretched_rows)
    for y in reversed(stretched_rows):
        galaxies = [(g[0], g[1] + expand_delta) if g[1] > y else g for g in galaxies]
    for x in reversed(stretched_columns):
        galaxies = [(g[0] + expand_delta, g[1]) if g[0] > x else g for g in galaxies]

    return sum(
        manhattan_distance(g, g2)
        for i, g in enumerate(galaxies[0:-1])
        for i2, g2 in enumerate(galaxies[i + 1 :])
    )


def part_one(lines) -> int:
    galaxies = parse_lines(lines)
    return calculate_distances(galaxies, 2 - 1)


def part_two(lines) -> int:
    galaxies = parse_lines(lines)
    return calculate_distances(galaxies, 1000000 - 1)


def main() -> None:
    with open("day11_input.txt", "r") as file:
        lines = file.read().splitlines()
        print(part_one(lines))
        print(part_two(lines))


if __name__ == "__main__":
    main()
