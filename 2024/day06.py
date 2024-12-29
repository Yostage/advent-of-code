import functools
import re
from collections import OrderedDict
from dataclasses import dataclass, field
from functools import cache
from itertools import cycle
from typing import Any, Deque, Dict, List, Set, Tuple, TypeVar

from CharacterGrid import CharacterGrid, Directions
from util import Point2D, tuple2_add

char_to_directions = {
    "^": Directions.UP,
    ">": Directions.RIGHT,
    "V": Directions.DOWN,
    "<": Directions.LEFT,
}

turn_order = [Directions.UP, Directions.RIGHT, Directions.DOWN, Directions.LEFT]

directions_to_char = {v: k for k, v in char_to_directions.items()}


def parse_lines(lines: List[str]) -> CharacterGrid:
    return CharacterGrid.from_lines(lines)


def part_one(lines) -> int:
    map = parse_lines(lines)
    (loc, _) = next((k, v) for k, v in map.map.items() if v == "^")
    direction_iterator = cycle(turn_order)
    current_facing = next(direction_iterator)
    while True:
        next_step = tuple2_add(loc, current_facing)
        next_contents = map.map.get(next_step)
        if next_contents == "#":
            current_facing = next(direction_iterator)
            continue
        map.map[loc] = "X"
        loc = next_step
        if next_contents is None:
            break

    return sum(1 for v in map.map.values() if v == "X")


def has_cycle(lines: List[str], added_obstacle: Point2D):
    map = parse_lines(lines)
    map.map[added_obstacle] = "#"
    direction_iterator = cycle(turn_order)
    current_facing = next(direction_iterator)
    (loc, _) = next((k, v) for k, v in map.map.items() if v == "^")
    visited = set()
    while True:
        if (loc, current_facing) in visited:
            return True
        visited.add((loc, current_facing))
        next_step = tuple2_add(loc, current_facing)
        next_contents = map.map.get(next_step)
        if next_contents == "#":
            current_facing = next(direction_iterator)
            continue
        loc = next_step

        if next_contents is None:
            return False


def part_two(lines) -> int:
    map = parse_lines(lines)
    # n.b. the full candidate list can be just the traversal from part 1
    candidates = [k for k, v in map.map.items() if v == "."]
    return sum(1 for c in candidates if has_cycle(lines, c))


def main() -> None:
    with open("day06_input.txt", "r") as file:
        lines = file.read().splitlines()
        print(part_one(lines))
        print(part_two(lines))


if __name__ == "__main__":
    main()
