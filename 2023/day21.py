import functools
import re
from dataclasses import dataclass, field
from functools import cache
from multiprocessing import Value
from typing import Any, Deque, Dict, List, Set, Tuple, TypeVar

from CharacterGrid import CharacterGrid, orthogonal_adjacencies
from util import Point2D, tuple2_add


def parse_lines(lines: List[str]) -> Any:
    return CharacterGrid.from_lines(lines)


def part_one(lines) -> int:
    grid = parse_lines(lines)

    if grid.max_x() == 10:
        steps = 6
    elif grid.max_x() == 130:
        steps = 64
    else:
        raise ValueError(grid.max_x())

    next_gen: Set[Point2D] = set(k for k, v in grid.map.items() if v == "S")
    assert len(next_gen) == 1
    for generation in range(steps):
        last_gen = next_gen
        next_gen = set()
        for space in last_gen:
            for adj in orthogonal_adjacencies:
                candidate = tuple2_add(space, adj)
                if grid.map.get(candidate) in ["S", "."]:
                    next_gen.add(candidate)
        # print(
        #     f"generation:{generation}: from {len(last_gen)} plots to {len(next_gen)} plots"
        # )

    return len(next_gen)


def part_two(lines) -> int:
    parse_lines(lines)
    return 0


def main() -> None:
    with open("day21_input.txt", "r") as file:
        lines = file.read().splitlines()
        print(part_one(lines))
        print(part_two(lines))


if __name__ == "__main__":
    main()
