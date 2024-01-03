import functools
import re
from collections import defaultdict, deque
from dataclasses import dataclass, field
from functools import cache
from typing import Any, Deque, Dict, List, Set, TypeVar

from CharacterGrid import CharacterGrid, Directions, orthogonal_adjacencies
from util import Point2D, tuple2_add

dmap = {
    "U": Directions.UP,
    "D": Directions.DOWN,
    "L": Directions.LEFT,
    "R": Directions.RIGHT,
}


def parse_lines(lines: List[str]) -> Any:
    result = []
    for line in lines:
        tokens = line.split(" ")
        result.append((tokens[0], tokens[1], tokens[2][2:-1]))

    return result


def part_one(lines) -> int:
    def flood_fill(map: Dict[Point2D, str], loc: Point2D) -> None:
        # permit us to be aggressive with the flood fill
        if map[loc] != ".":
            return

        visited: Set[Point2D] = set()
        queue: Deque[Point2D] = deque()
        queue.append(loc)

        inside = True
        while len(queue) > 0:
            visiting = queue.pop()
            visited.add(visiting)

            for edge in orthogonal_adjacencies:
                target = tuple2_add(visiting, edge)

                if target not in map:
                    inside = False
                    continue

                if target not in visited and target not in queue and map[target] == ".":
                    queue.append(target)

            # if we're adjacent to any edges, we are outside
            # enqueue any adjacent empty spaces

        # finally, color all the spaces
        for pt in visited:
            map[pt] = "I" if inside else "o"

    def mark_inside(map: Dict[Point2D, str], loc: Point2D) -> None:
        ray_trace = "".join(
            [
                # all the pipe segments
                map[(loc[0], y)]
                # from where we are up to y=0
                for y in range(loc[1], -1, -1)
                # only intersect things on the path
                # if distances[(loc[0], y)] != max_int
                # if map[(loc[0], y)] == "#"
            ]
        )
        ray_trace = ray_trace.replace("o", ".")
        # now compress the runs down
        ray_trace = re.sub(r"#{2,}", "", ray_trace)
        ray_trace = re.sub(r"\.+", ".", ray_trace)
        ray_trace = ray_trace.replace(".", "")

        # odd number of intersections means inside
        if (len(ray_trace) % 2) == 1:
            map[loc] = "o"

    lines = parse_lines(lines)

    grid = CharacterGrid(map=defaultdict(lambda: "."))
    digger = (0, 0)
    grid.map[digger] = "#"
    for line in lines:
        (dir_tok, magnitude, color) = line
        for _ in range(int(magnitude)):
            digger = tuple2_add(digger, dmap[dir_tok])
            grid.map[digger] = "#"
        # print(line)
        # grid.render()

    grid.render()

    for x in range(grid.min_x(), grid.width()):
        for y in range(grid.min_y(), grid.height()):
            if grid.map[(x, y)] == ".":
                flood_fill(grid.map, (x, y))

    grid.render()

    return sum(1 for x in grid.map.values() if x not in ("o", "."))


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
