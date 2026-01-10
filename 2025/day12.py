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
    def does_region_fit(region):
        ((width, height), present_requirements) = region
        available_size = width * height

        tiled_size = sum(
            present_requirement * grid_square_sizes[i]
            for i, present_requirement in enumerate(present_requirements)
        )
        if available_size >= tiled_size:
            return True

        minimum_x = sum(
            present_requirement * grid_xes[i]
            for i, present_requirement in enumerate(present_requirements)
        )
        print(f"{minimum_x} to fit in {available_size}: {minimum_x <= available_size}")
        if minimum_x > available_size:
            return False

        # base case
        print("unknown region")
        print(region)
        return None

    (grids, regions) = parse_lines(lines)
    # for grid in grids:
    # grid.render()
    grid_xes = [sum(1 if v == "#" else 0 for v in grid.map.values()) for grid in grids]
    grid_square_sizes = [grid.width() * grid.height() for grid in grids]
    # for idx, size in enumerate(grid_sizes):
    # print(f"{idx} : {size}")

    total = 0

    return sum(1 if does_region_fit(region) else 0 for region in regions)

    # print(regions)

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
