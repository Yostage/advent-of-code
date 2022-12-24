import functools
import re
from dataclasses import dataclass, field
from functools import cache
from typing import Any, Dict, List, Set, Tuple, TypeVar

Point3D = Tuple[int, int, int]

CubeSet = Set[Point3D]


def parse_lines(lines: List[str]) -> CubeSet:
    cubes: Set[Point3D] = set()
    for line in lines:
        strings = line.split(",")
        cubes.add(tuple(map(int, strings)))  # type: ignore

    return cubes


def part_one(lines) -> int:
    cubes = parse_lines(lines)
    open_sides = 0
    for cube in cubes:
        for side in [
            (1, 0, 0),
            (-1, 0, 0),
            (0, 1, 0),
            (0, -1, 0),
            (0, 0, 1),
            (0, 0, -1),
        ]:
            test = tuple(map(sum, zip(cube, side)))  # type: ignore
            if not test in cubes:
                # print(f"Open side {test}")
                open_sides += 1
    return open_sides


def part_two(lines) -> int:
    parse_lines(lines)
    return 0


def main() -> None:
    with open("day18_input.txt", "r") as file:
        lines = file.read().splitlines()
        print(part_one(lines))
        print(part_two(lines))


if __name__ == "__main__":
    main()
