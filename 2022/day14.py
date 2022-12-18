import functools
import re
from collections import defaultdict
from dataclasses import dataclass, field
from functools import cache
from typing import Any, Dict, List, Tuple, TypeVar


def parse_lines(lines: List[str]) -> List[List[Tuple[int, int]]]:
    segments: List[List[Tuple[int, int]]] = []
    for line in lines:
        coords = line.split(" -> ")
        segment: List[Tuple[int, int]] = []
        for coord in coords:
            (x, y) = [int(k) for k in coord.split(",")]
            segment.append((x, y))
        segments.append(segment)

        # points = [coord.split(",") for coord in coords]
        # segments.append([coord.split(",") for coord in coords])

    # print(segments)
    return segments


def lerp(t: int, times: Tuple[int, int], points: List[Tuple[int, int]]):
    dx = points[1][0] - points[0][0]
    dy = points[1][1] - points[0][1]
    dt = (t - times[0]) / (times[1] - times[0])
    return dt * dx + points[0][0], dt * dy + points[0][1]


def part_one(lines) -> int:
    scanner = defaultdict(lambda: ".")
    segments = parse_lines(lines)
    # build walls
    for segment in segments:
        start = segment.pop(0)

        while len(segment) > 0:
            end = segment.pop(0)
            wall_length = abs(end[0] - start[0]) + abs(end[1] - start[1])
            assert wall_length > 0
            for t in range(0, wall_length + 1):
                wall = lerp(t=t, times=(0, wall_length), points=[start, end])
                # print(f"{start} to {end} at t={t} = {wall}")
                # lerp makes floats
                # int_tup =
                scanner[tuple(map(int, wall))] = "#"
            start = end

    # drop sand
    max_y = max(k[1] for k, v in scanner.items() if v == "#")
    sand_start = (500, 0)
    sand_dropped = 0
    sand_lost = False
    while not sand_lost:

        def test_empty(loc: Tuple[int, int]) -> bool:
            return scanner[loc] == "."

        sand = sand_start
        while True:
            if sand[1] >= max_y:
                # termination condition
                sand_lost = True
                break
            # test down
            # for candidate in [(sand[0], sand[1] + 1), (sand[0]-1, sand[1] + 1), (sand[0]+2, sand[1] + 1)]:
            #     if test_empty(candidate):
            #         sand=candidiate
            elif test_empty((sand[0], sand[1] + 1)):
                sand = (sand[0], sand[1] + 1)
            # test downleft
            elif test_empty((sand[0] - 1, sand[1] + 1)):
                sand = (sand[0] - 1, sand[1] + 1)
            # test downright
            elif test_empty((sand[0] + 1, sand[1] + 1)):
                sand = (sand[0] + 1, sand[1] + 1)
            # we gotta stop!
            else:
                scanner[sand] = "o"
                sand_dropped += 1
                break

    # check down
    # check down-left
    # check down-right
    # if all are blocked
    # set o, increment dropped sand
    # if y has reached 100, we're falling FOREVER
    # terminate

    # render
    min_x = min(k[0] for k, v in scanner.items() if v != ".")
    max_x = max(k[0] for k, v in scanner.items() if v != ".")
    min_y = min(k[1] for k, v in scanner.items() if v != ".")
    max_y = max(k[1] for k, v in scanner.items() if v != ".")
    for y in range(min_y, max_y + 1):
        print("".join([scanner[(x, y)] for x in range(min_x, max_x + 1)]))

    return sand_dropped


def part_two(lines) -> int:
    parse_lines(lines)
    return 0


def main() -> None:
    with open("day14_input.txt", "r") as file:
        lines = file.read().splitlines()
        print(part_one(lines))
        print(part_two(lines))


if __name__ == "__main__":
    main()
