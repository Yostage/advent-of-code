import functools
import re
from collections import defaultdict, deque
from dataclasses import dataclass, field
from functools import cache
from typing import Any, Deque, Dict, List, Mapping, Sequence, Set, TypeVar

from util import Point2D, tuple2_add

adjacencies = {
    "|": ((0, 1), (0, -1)),
    "-": ((1, 0), (-1, 0)),
    "L": ((0, -1), (1, 0)),
    "J": ((0, -1), (-1, 0)),
    "7": ((0, 1), (-1, 0)),
    "F": ((0, 1), (1, 0)),
    ".": tuple(),
}


@dataclass
class PipeMaze:
    start: Point2D
    map: Mapping[Point2D, Sequence[Point2D]]


def parse_lines(lines: List[str]) -> Any:
    map: Dict[Point2D, Sequence[Point2D]] = {}
    start = None
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            if c == "S":
                start = (x, y)
                map[(x, y)] = []
            else:
                # convert the adjacencies to actual edges
                map[(x, y)] = [tuple2_add((x, y), adj) for adj in adjacencies[c]]
    assert start is not None
    return PipeMaze(start=start, map=map)


def part_one(lines) -> int:
    maze = parse_lines(lines)
    # first calculate the shape of our starting place
    for orthogonal_dir in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
        # backlink to anybody who links to us
        adjacent_space = tuple2_add(maze.start, orthogonal_dir)
        if adjacent_space in maze.map and maze.start in maze.map[adjacent_space]:
            maze.map[maze.start].append(adjacent_space)

    # better be only two links out
    assert len(maze.map[maze.start]) == 2

    # now visit all the spaces until we're done, and fetch the highest space
    max_int = 99999999999
    distances: Dict[Point2D, int] = defaultdict(lambda: max_int)
    unvisited: Deque = deque()
    unvisited.append(maze.start)
    distances[maze.start] = 0
    visited: Set[Point2D] = set()

    def pretty_cell(x, y, visiting):
        if distances[(x, y)] == max_int:
            return "."
        if (x, y) == visiting:
            return "*"
        return str(distances[(x, y)])

    while len(unvisited) > 0:
        visiting = unvisited.pop()
        visited.add(visiting)
        for adjacent in maze.map[visiting]:
            distances[adjacent] = min(distances[adjacent], distances[visiting] + 1)
            if adjacent not in visited and adjacent not in unvisited:
                unvisited.appendleft(adjacent)

    #     for y in range(len(lines)):
    #         print("".join([pretty_cell(x, y, visiting) for x in range(len(lines[0]))]))
    #     print()

    # for y in range(len(lines)):
    #     print("".join([pretty_cell(x, y, (-1, -1)) for x in range(len(lines[0]))]))

    return max([x for x in distances.values() if x != max_int])


def part_two(lines) -> int:
    parse_lines(lines)
    return 0


def main() -> None:
    with open("day10_input.txt", "r") as file:
        lines = file.read().splitlines()
        print(part_one(lines))
        print(part_two(lines))


if __name__ == "__main__":
    main()
