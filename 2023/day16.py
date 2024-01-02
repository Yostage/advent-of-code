import functools
import re
from ast import Lambda
from collections import deque
from dataclasses import dataclass, field
from functools import cache
from typing import Any, Callable, Deque, Dict, Iterable, List, Set, Tuple, TypeVar

from CharacterGrid import CharacterGrid, orthogonal_adjacencies
from util import Point2D, tuple2_add


def parse_lines(lines: List[str]) -> CharacterGrid:
    return CharacterGrid.from_lines(lines)


# -
def h_splitter(in_dir: Point2D) -> List[Point2D]:
    if in_dir[1] == 0:
        return [in_dir]
    else:
        return [(-1, 0), (1, 0)]


# |
def v_splitter(in_dir: Point2D) -> List[Point2D]:
    if in_dir[0] == 0:
        return [in_dir]
    else:
        return [(0, 1), (0, -1)]


# for each piece and your incoming direction, we tell you the translations and directions to go next
bounce_map: Dict[str, Callable[[Point2D], List[Point2D]]] = {
    "\\": lambda x: [(x[1], x[0])],
    "/": lambda x: [(-x[1], -x[0])],
    "-": h_splitter,
    "|": v_splitter,
    ".": lambda x: [x],
}


def part_one(lines) -> int:
    grid = parse_lines(lines)
    start_pos = (0, 0)
    start_dir = (1, 0)
    visit_queue: Deque[Tuple[Point2D, Point2D]] = deque([(start_pos, start_dir)])
    lit: Set[Point2D] = set([(0, 0)])
    loop: Set[Tuple[Point2D, Point2D]] = set()

    while len(visit_queue) > 0:
        (pos, dir) = visit_queue.pop()
        lit.add(pos)

        dirs = bounce_map[grid.map[pos]](dir)
        for new_dir in dirs:
            new_pos = tuple2_add(pos, new_dir)
            # bounced off the map
            if new_pos not in grid.map:
                continue

            next_state = (new_pos, new_dir)

            # have already processed this state
            if next_state in loop:
                continue
            loop.add((pos, dir))
            visit_queue.append(next_state)

    return len(lit)


def part_two(lines) -> int:
    parse_lines(lines)
    return 0


def main() -> None:
    with open("day16_input.txt", "r") as file:
        lines = file.read().splitlines()
        print(part_one(lines))
        print(part_two(lines))


if __name__ == "__main__":
    main()
