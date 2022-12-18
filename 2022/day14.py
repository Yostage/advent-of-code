import functools
import re
from collections import defaultdict
from dataclasses import dataclass, field
from functools import cache
from typing import Any, Dict, List, Tuple, TypeVar


class Scanner:
    # map: Dict[Tuple[int, int], str] = field(default_factory=defaultdict(lambda: "."))
    map: defaultdict[Tuple[int, int], str]

    def __init__(self):
        self.map = defaultdict(lambda: ".")

    def test_empty(self, loc: Tuple[int, int]) -> bool:
        return self.map[loc] == "."

    def build_walls(self, segments: List[List[Tuple[int, int]]]) -> None:
        for segment in segments:
            start = segment.pop(0)

            while len(segment) > 0:
                end = segment.pop(0)
                wall_length = abs(end[0] - start[0]) + abs(end[1] - start[1])
                assert wall_length > 0
                for t in range(0, wall_length + 1):
                    wall = lerp(t=t, times=(0, wall_length), points=[start, end])
                    self.map[tuple(map(int, wall))] = "#"  # type: ignore
                start = end

    def render(self):
        print()
        min_x = min(k[0] for k, v in self.map.items() if v != ".")
        max_x = max(k[0] for k, v in self.map.items() if v != ".")
        min_y = min(k[1] for k, v in self.map.items() if v != ".")
        max_y = max(k[1] for k, v in self.map.items() if v != ".")
        for y in range(min_y, max_y + 1):
            print("".join([self.map[(x, y)] for x in range(min_x, max_x + 1)]))
        print()


def parse_lines(lines: List[str]) -> List[List[Tuple[int, int]]]:
    segments: List[List[Tuple[int, int]]] = []
    for line in lines:
        coords = line.split(" -> ")
        segment: List[Tuple[int, int]] = []
        for coord in coords:
            (x, y) = [int(k) for k in coord.split(",")]
            segment.append((x, y))
        segments.append(segment)

    # print(segments)
    return segments


def lerp(t: int, times: Tuple[int, int], points: List[Tuple[int, int]]):
    dx = points[1][0] - points[0][0]
    dy = points[1][1] - points[0][1]
    dt = (t - times[0]) / (times[1] - times[0])
    return dt * dx + points[0][0], dt * dy + points[0][1]


def part_one(lines) -> int:
    scanner = Scanner()
    segments = parse_lines(lines)
    scanner.build_walls(segments)

    # drop sand
    max_y = max(k[1] for k, v in scanner.map.items() if v == "#")
    sand_start = (500, 0)
    sand_dropped = 0
    sand_lost = False
    while not sand_lost:

        sand = sand_start
        sand_dropped += 1
        while True:
            if sand[1] >= max_y:
                # termination condition
                sand_lost = True
                break
            elif scanner.test_empty((sand[0], sand[1] + 1)):
                sand = (sand[0], sand[1] + 1)
            # test downleft
            elif scanner.test_empty((sand[0] - 1, sand[1] + 1)):
                sand = (sand[0] - 1, sand[1] + 1)
            # test downright
            elif scanner.test_empty((sand[0] + 1, sand[1] + 1)):
                sand = (sand[0] + 1, sand[1] + 1)
            # we gotta stop!
            else:
                scanner.map[sand] = "o"
                break

    scanner.render()

    return sand_dropped - 1


def part_two(lines) -> int:
    scanner = Scanner()
    segments = parse_lines(lines)
    scanner.build_walls(segments)

    # drop sand
    max_y = max(k[1] for k, v in scanner.map.items() if v == "#")
    sand_start = (500, 0)
    sand_dropped = 0

    while scanner.map[sand_start] != "o":
        sand = sand_start
        while True:
            if sand[1] == max_y + 1:
                # we hit the virtual floor
                break
            elif scanner.test_empty((sand[0], sand[1] + 1)):
                sand = (sand[0], sand[1] + 1)
            elif scanner.test_empty((sand[0] - 1, sand[1] + 1)):
                sand = (sand[0] - 1, sand[1] + 1)
            elif scanner.test_empty((sand[0] + 1, sand[1] + 1)):
                sand = (sand[0] + 1, sand[1] + 1)
            elif sand == sand_start:
                # sand landed at sand_start
                break
            else:
                # we hit the real floor
                break

        assert scanner.map[sand] != "o"
        scanner.map[sand] = "o"
        sand_dropped = sand_dropped + 1

    scanner.render()

    return sum([1 if v == "o" else 0 for v in scanner.map.values()])


def main() -> None:
    with open("day14_input.txt", "r") as file:
        lines = file.read().splitlines()
        print(part_one(lines))
        print(part_two(lines))


if __name__ == "__main__":
    main()
