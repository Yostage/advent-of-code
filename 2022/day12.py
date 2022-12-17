import functools
import re
from collections import defaultdict
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

    path_back: "Optional[MapNode]" = None

    def pos(self) -> Tuple[int, int]:
        return (self.x, self.y)

    # def printable_distance(self) -> str:
    #     if self.best_distance > 1000:
    #         return "!!"
    #     else:
    #         return f"{self.best_distance:02d}"

    def __key(self):
        return (self.x, self.y, self.height)

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        if isinstance(other, MapNode):
            return self.__key() == other.__key()
        return NotImplemented


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


def shortest_path(map: Map, start_pos: Tuple[int, int], end_pos: Tuple[int, int]):
    max_distance = 2**16
    distances = defaultdict(lambda: max_distance)

    start_node = map.at(start_pos)
    distances[start_pos] = 0
    unvisited = [start_node]

    # does equality work
    assert map.at(start_pos) == map.at(start_pos)
    assert map.at(start_pos) != map.at(end_pos)

    while len(unvisited) > 0:
        v = unvisited.pop(0)
        v.visited = True

        # print(f"Visiting {v.x}, {v.y}")
        for adj in v.neighbors:
            new_distance = distances[v.pos()] + 1
            # is this a new good edge?
            if distances[adj.pos()] > new_distance:

                distances[adj.pos()] = new_distance
                adj.path_back = v
                unvisited.append(adj)

                # termination condition
                if adj == map.at(map.end_pos):
                    return distances[adj.pos()]

    # raise AssertionError("No path found")
    # no path found (sus)
    return max_distance


def part_one(lines) -> int:
    map = parse_lines(lines)
    return shortest_path(map, map.start_pos, map.end_pos)


def part_two(lines) -> int:
    map = parse_lines(lines)
    # possible_starts = nodes where node.height = start_height
    starts = [
        (x, y)
        for x in range(len(map.nodes[0]))
        for y in range(len(map.nodes))
        if map.at((x, y)).height == map.at(map.start_pos).height
    ]
    print(f"possible starts = {starts}")
    shortest_paths = [shortest_path(map, start, map.end_pos) for start in starts]
    return min(shortest_paths)


def main() -> None:
    with open("day12_input.txt", "r") as file:
        lines = file.read().splitlines()
        print(part_one(lines))
        print(part_two(lines))


if __name__ == "__main__":
    main()
