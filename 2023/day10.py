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
    map: Mapping[Point2D, List[Point2D]]
    graphical_map: Mapping[Point2D, str]


orthogonal_adjacencies = [(1, 0), (0, 1), (-1, 0), (0, -1)]
max_int = 99999999999


def parse_lines(lines: List[str]) -> Any:
    map: Dict[Point2D, List[Point2D]] = {}
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

    # calculate the shape of our starting place
    for orthogonal_dir in orthogonal_adjacencies:
        # backlink to anybody who links to us
        adjacent_space = tuple2_add(start, orthogonal_dir)
        if adjacent_space in map and start in map[adjacent_space]:
            map[start].append(adjacent_space)

    # better be only two links out
    assert len(map[start]) == 2

    return PipeMaze(
        start=start,
        map=map,
        graphical_map={
            (x, y): c for y, line in enumerate(lines) for x, c in enumerate(line)
        },
    )


def part_one(lines) -> int:
    maze = parse_lines(lines)

    # now visit all the spaces until we're done, and fetch the highest space

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
    maze = parse_lines(lines)

    # now visit all the spaces until we're done, and fetch the highest space
    distances: Dict[Point2D, int] = defaultdict(lambda: max_int)
    unvisited: Deque = deque()
    unvisited.append(maze.start)
    distances[maze.start] = 0
    visited: Set[Point2D] = set()
    inside_edges: Dict[Point2D, Set[Point2D]] = defaultdict(lambda: set())

    # def pretty_cell(x, y, visiting):
    #     if distances[(x, y)] == max_int:
    #         return "."
    #     if (x, y) == visiting:
    #         return "*"
    #     return str(distances[(x, y)])

    # visit the whole loop
    while len(unvisited) > 0:
        visiting = unvisited.pop()
        visited.add(visiting)
        for adjacent in maze.map[visiting]:
            distances[adjacent] = min(distances[adjacent], distances[visiting] + 1)
            if adjacent not in visited and adjacent not in unvisited:
                unvisited.appendleft(adjacent)

    def flood_fill(start: Point2D) -> None:
        visit_queue: Deque = deque([start])
        # visit_queue.append(start)
        visited: Set[Point2D] = set()
        assert maze.graphical_map[start] == "."
        leaked = False
        logged = {(2, 6), (3, 6)}
        while len(visit_queue) > 0:
            visiting = visit_queue.pop()
            visited.add(visiting)

            for adjacent in [
                tuple2_add(visiting, adj) for adj in orthogonal_adjacencies
            ]:
                if (
                    adjacent in maze.graphical_map
                    and maze.graphical_map[adjacent] == "."
                ):
                    if adjacent not in visit_queue and adjacent not in visited:
                        visit_queue.appendleft(adjacent)
                # off the map
                elif adjacent not in maze.graphical_map:
                    leaked = True
                    if visiting in logged:
                        print(
                            f"Marking leak on {visiting} because {adjacent} not in map"
                        )
                # not in the loop
                elif distances[adjacent] == max_int:
                    if visiting in logged:
                        print(
                            f"Marking leak on {visiting} because {adjacent} not in loop"
                        )
                    leaked = True
        # execute flood fill
        for loc in visited:
            # if leaked:
            #     print(f"Marking {loc} outside")
            # else:
            #     print(f"marking {loc} inside")
            maze.graphical_map[loc] = "O" if leaked else "I"

    while unflooded := next(
        (loc for loc in maze.graphical_map if maze.graphical_map[loc] == "."), None
    ):
        flood_fill(unflooded)

    def render_visited(loc: Point2D):
        if loc in {(2, 6), (3, 6)}:
            # if loc == (3, 7):
            # print(f"{loc} distance = {distances[loc]}")
            return "X"
        if distances[loc] != max_int:
            return "*"
        else:
            return "."

    def render(loc: Point2D):
        # if distances[loc] != max_int:
        #     return "*"
        # else:
        return maze.graphical_map[loc]

    print()
    for y in range(len(lines)):
        print("".join([render_visited((x, y)) for x in range(len(lines[0]))]))
    print()
    print()
    for y in range(len(lines)):
        print("".join([render((x, y)) for x in range(len(lines[0]))]))
    print()

    # for y in range(len(lines)):
    #     print("".join([pretty_cell(x, y, (-1, -1)) for x in range(len(lines[0]))]))

    return sum([1 for cell in maze.graphical_map.values() if cell == "I"])


def main() -> None:
    with open("day10_input.txt", "r") as file:
        lines = file.read().splitlines()
        print(part_one(lines))
        print(part_two(lines))


if __name__ == "__main__":
    main()
