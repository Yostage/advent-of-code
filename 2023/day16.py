from collections import deque
from itertools import chain
from typing import Callable, Deque, Dict, List, Set, Tuple

from CharacterGrid import CharacterGrid
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


# given an input direction and a square, which directions do we go to
bounce_map: Dict[str, Callable[[Point2D], List[Point2D]]] = {
    "\\": lambda x: [(x[1], x[0])],
    "/": lambda x: [(-x[1], -x[0])],
    "-": h_splitter,
    "|": v_splitter,
    ".": lambda x: [x],
}


def count_lit(grid, start_pos, start_dir) -> int:
    visit_queue: Deque[Tuple[Point2D, Point2D]] = deque([(start_pos, start_dir)])
    lit: Set[Point2D] = set()
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


def part_one(lines) -> int:
    grid = parse_lines(lines)
    return count_lit(grid, (0, 0), (1, 0))


def part_two(lines) -> int:
    grid = parse_lines(lines)
    tops = [count_lit(grid, (x, 0), (0, 1)) for x in range(0, grid.width())]
    bottoms = [
        count_lit(grid, (x, grid.max_y()), (0, -1)) for x in range(0, grid.width())
    ]
    lefts = [count_lit(grid, (0, y), (1, 0)) for y in range(0, grid.height())]
    rights = [
        count_lit(grid, (grid.max_x(), y), (-1, 0)) for y in range(0, grid.height())
    ]
    return max(chain(tops, bottoms, lefts, rights))


def main() -> None:
    with open("day16_input.txt", "r") as file:
        lines = file.read().splitlines()
        print(part_one(lines))
        print(part_two(lines))


if __name__ == "__main__":
    main()
