import functools
import re
from dataclasses import dataclass, field
from functools import cache
from typing import Any, Dict, List, Optional, Set, Tuple, TypeVar


@dataclass
class MapNode:
    x: int
    y: int
    neighbors: "Set[MapNode]"
    height: int
    visited: bool = False
    best_distance: int = 2**16
    path_back: "Optional[MapNode]" = None

    def printable_distance(self) -> str:
        if self.best_distance > 1000:
            return "!!"
        else:
            return f"{self.best_distance:02d}"

    def __key(self):
        return (self.x, self.y, self.height)

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        if isinstance(other, MapNode):
            return self.__key() == other.__key()
        return NotImplemented

    # def linkTo(self, m: "MapNode"):
    #     m.neighbors.add(self)
    #     self.neighbors.add(m)


@dataclass
class Map:
    heights: List[List[int]]
    start_pos = (-1, -1)
    end_pos = (-1, -1)

    def at(self, loc: Tuple[int, int]) -> MapNode:
        return self.nodes[loc[1]][loc[0]]

    nodes: List[List[MapNode]]


def parse_lines(lines: List[str]) -> Map:

    map = Map(heights=[], nodes=[])
    for line in lines:
        map.heights.append([ord(c) for c in line])

    # print(map.heights)

    # fix up start and end
    for y, heightline in enumerate(map.heights):
        for x, c in enumerate(heightline):
            if c == ord("S"):
                map.start_pos = (x, y)
                map.heights[y][x] = ord("a")
            if c == ord("E"):
                map.end_pos = (x, y)
                map.heights[y][x] = ord("z")

    assert map.start_pos != (-1, -1)
    assert map.end_pos != (-1, -1)

    # let's make nodes instead
    for y, heightline in enumerate(map.heights):
        map.nodes.append(
            [
                MapNode(x=x, y=y, height=c, neighbors=set())
                for x, c in enumerate(heightline)
            ]
        )

    # link up the edges
    for y, nodeline in enumerate(map.nodes):
        for x, node in enumerate(nodeline):
            for targetx, targety in [(x, y + 1), (x, y - 1), (x + 1, y), (x - 1, y)]:
                if targetx in range(0, len(nodeline)) and targety in range(
                    0, len(map.nodes)
                ):
                    adj = map.at((targetx, targety))
                    if (adj.height - node.height) <= 1:
                        node.neighbors.add(adj)
                        # print(f"Found edge from {(x,y)} --> {(targetx, targety)} ")

    return map


def part_one(lines) -> int:

    map = parse_lines(lines)

    start = map.at(map.start_pos)
    start.best_distance = 0
    unvisited = [map.at(map.start_pos)]

    # does equality work
    assert map.at(map.start_pos) == map.at(map.start_pos)
    assert map.at(map.start_pos) != map.at(map.end_pos)

    while len(unvisited) > 0:
        v = unvisited.pop(0)
        v.visited = True

        # print(f"Visiting {v.x}, {v.y}")
        for adj in v.neighbors:

            # is this a new good edge?
            if adj.best_distance > v.best_distance + 1:

                adj.best_distance = v.best_distance + 1
                adj.path_back = v
                unvisited.append(adj)

                if adj == map.at(map.end_pos):
                    return adj.best_distance

    # heights
    for nodeline in map.nodes:
        print(" ".join([f"{n.height:02d}" for n in nodeline]))
    print()
    # dump final map
    for nodeline in map.nodes:
        print(" ".join([n.printable_distance() for n in nodeline]))

    assert False
    # find the length of the path to end
    # unvisited = start
    # for each node in unvisited
    #   visit()
    # visit:
    # unvisited += all neighbors
    # if min_dist < min_dist = dist + 1
    #   min_dist = dist+1
    #   path_back = parent
    #   if we just visited the dest, return distance

    return 0


def part_two(lines) -> int:
    parse_lines(lines)
    return 0


def main() -> None:
    with open("day12_input.txt", "r") as file:
        lines = file.read().splitlines()
        print(part_one(lines))
        print(part_two(lines))


if __name__ == "__main__":
    main()
