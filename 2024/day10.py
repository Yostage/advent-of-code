import functools
import re
from collections import deque
from dataclasses import dataclass, field
from functools import cache
from typing import Any, Deque, Dict, List, Set, Tuple, TypeVar

from CharacterGrid import CharacterGrid, orthogonal_adjacencies
from util import Point2D, tuple2_add


def parse_lines(lines: List[str]) -> CharacterGrid:
    return CharacterGrid.from_lines(lines)


def find_the_nines(start: Point2D, grid: CharacterGrid) -> int:
    map = grid.map
    visited = set()
    to_visit = deque([start])
    nines_found = 0
    while to_visit:
        loc = to_visit.popleft()
        if loc in visited:
            continue
        visited.add(loc)
        if map[loc] == "9":
            nines_found += 1
            continue
        for direction in orthogonal_adjacencies:
            new_loc = tuple2_add(loc, direction)
            if new_loc in map:
                if int(map[new_loc]) == int(map[loc]) + 1:
                    to_visit.append(new_loc)
    return nines_found


def part_one(lines) -> int:
    grid = parse_lines(lines)
    # for every zero in the grid
    # search how many nines are reachable, with single step increasing walk
    return sum(find_the_nines(loc, grid) for loc, val in grid.map.items() if val == "0")


def find_all_paths_to_nines(start: Point2D, grid: CharacterGrid) -> int:
    map = grid.map
    to_visit: Deque[Tuple[Point2D, ...]] = deque([(start,)])
    paths_found = 0
    while to_visit:
        path = to_visit.popleft()
        final_step = path[-1]
        if map[final_step] == "9":
            paths_found += 1
            continue
        for direction in orthogonal_adjacencies:
            new_loc = tuple2_add(final_step, direction)
            if new_loc in map:
                if int(map[new_loc]) == int(map[final_step]) + 1:
                    to_visit.append(path + (new_loc,))
    return paths_found


def part_two(lines) -> int:
    grid = parse_lines(lines)
    return sum(
        find_all_paths_to_nines(loc, grid)
        for loc, val in grid.map.items()
        if val == "0"
    )


def main() -> None:
    with open("day10_input.txt", "r") as file:
        lines = file.read().splitlines()
        print(part_one(lines))
        print(part_two(lines))


if __name__ == "__main__":
    main()
