import functools
import re
from dataclasses import dataclass, field
from functools import cache

from CharacterGrid import CharacterGrid


def parse_lines(lines: list[str]):
    def eat_grid(iter):
        new_grid = []
        for line in line_iter:
            if line == "":
                return CharacterGrid.from_lines(new_grid)
            else:
                new_grid.append(line)

    line_iter = iter(lines)
    grids = []
    regions = []
    for line in line_iter:
        if line[1] == ":":
            grids.append(eat_grid(line_iter))
        if "x" in line:
            (left, right) = line.split(":")
            width, height = left.split("x")
            present_requirements = tuple(map(int, right.split()))
            regions.append(((int(width), int(height)), present_requirements))

    return (grids, regions)


def part_one(lines) -> int:
    (grids, regions) = parse_lines(lines)
    for grid in grids:
        grid.render()
    print(regions)
    total = 0
    return total


def part_two(lines) -> int:
    parse_lines(lines)
    total = 0
    return total


def main() -> None:
    with open("day12_input.txt", "r") as file:
        lines = file.read().splitlines()
        # not zero
        print(part_one(lines))
        print(part_two(lines))


if __name__ == "__main__":
    main()
