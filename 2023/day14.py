import functools
import re
from dataclasses import dataclass, field
from functools import cache
from typing import Any, Dict, List, TypeVar

from util import Point2D

CharacterGrid2D = Dict[Point2D, str]


@dataclass
class CharacterGrid:
    map: CharacterGrid2D

    def max_x(self) -> int:
        return max(pt[0] for pt in self.map.keys())

    def max_y(self) -> int:
        return max(pt[1] for pt in self.map.keys())

    def width(self) -> int:
        return self.max_x() + 1

    def height(self) -> int:
        return self.max_y() + 1

    def render(self) -> None:
        print()
        for y in range(self.height()):
            print("".join([self.map[(x, y)] for x in range(self.width())]))
        print()


def parse_lines(lines: List[str]) -> CharacterGrid:
    return CharacterGrid(
        map={(x, y): c for y, line in enumerate(lines) for x, c in enumerate(line)}
    )


def calculate_score(map: CharacterGrid) -> int:
    sum = 0
    for (x, y), v in map.map.items():
        if v == "O":
            sum += map.max_y() + 1 - y

    return sum


def shift_all_rocks(map: CharacterGrid, direction: Point2D = (0, -1)) -> None:
    # it's important that we iterate in order
    for x in range(0, map.width()):
        for y in range(0, map.height()):
            if map.map[(x, y)] != "O":
                continue
            new_y = y - 1
            while new_y >= 0 and map.map[(x, new_y)] == ".":
                new_y -= 1
            map.map[(x, y)] = "."
            map.map[(x, new_y + 1)] = "O"


def part_one(lines) -> int:
    map = parse_lines(lines)
    map.render()
    shift_all_rocks(map)
    map.render()

    return calculate_score(map)


def part_two(lines) -> int:
    parse_lines(lines)
    return 0


def main() -> None:
    with open("day14_input.txt", "r") as file:
        lines = file.read().splitlines()
        print(part_one(lines))
        print(part_two(lines))


if __name__ == "__main__":
    main()
