import functools
import itertools
import re
from collections import defaultdict, deque
from dataclasses import dataclass, field
from functools import cache
from typing import Any, DefaultDict, Dict, List, Tuple, TypeVar

from day15 import Point2D
from day22 import tuple2_add


class GroveMap:
    map: defaultdict[Point2D, str]

    def __init__(self):
        self.map = defaultdict(lambda: ".")

    def get_bounding_box(self) -> Tuple[Point2D, Point2D]:
        mins = [
            min([loc[c] for loc, str in self.map.items() if str == "#"]) for c in [0, 1]
        ]
        maxes = [
            max([loc[c] for loc, str in self.map.items() if str == "#"]) for c in [0, 1]
        ]
        return (tuple(mins), tuple(maxes))  # type: ignore

    def test_empty(self, loc: Point2D) -> bool:
        if not loc in self.map:
            return True
        # avoid overpopulating the map
        return self.map[loc] == "."

    def render(self) -> None:
        # by_y = itertools.groupby(
        #     sorted(self.map, key=lambda p: p[1]), key=lambda p: p[1]
        # )
        # for _, row in by_y:
        #     px = list(row)
        #     buffer = ""
        #     for idx, pt in enumerate(sorted(px)):
        #         buffer += self.map[pt]
        #     print(buffer)
        (min, max) = self.get_bounding_box()
        for y in range(min[1], max[1] + 1):
            print(
                "".join(
                    "." if self.test_empty((x, y)) else "#"
                    for x in range(min[0], max[0] + 1)
                )
            )

        # result = sum(
        #     1 if grove.test_empty((x, y)) else 0
        #     for x in range(min[0], max[0] + 1)
        #     for y in range(min[1], max[1] + 1)
        # )

    direction_map = {
        "n": (0, -1),
        "s": (0, 1),
        "w": (-1, 0),
        "e": (1, 0),
    }

    def test_move(self, loc: Point2D, direction: str) -> bool:
        h_spread = [(i, 0) for i in range(-1, 2)]
        v_spread = [(0, i) for i in range(-1, 2)]
        if direction in ["n", "s"]:
            spread = h_spread
        else:
            spread = v_spread
        targets = [
            tuple2_add(loc, tuple2_add(self.direction_map[direction], spray))
            for spray in spread
        ]
        # return all targets empty
        return all(map(self.test_empty, targets))

    def surroundings_empty(self, loc: Point2D) -> bool:
        for x in range(-1, 2):
            for y in range(-1, 2):
                if x == 0 and y == 0:
                    continue
                if not self.test_empty(tuple2_add(loc, (x, y))):
                    return False
        return True


def parse_lines(lines: List[str]) -> GroveMap:
    grove = GroveMap()
    for y, line in enumerate(lines):
        for idx, s in enumerate(line):
            grove.map[(idx, y)] = s

    return grove


def part_one(lines) -> int:
    grove = parse_lines(lines)
    grove.render()
    moves = ["n", "s", "w", "e"]

    for round in range(0, 10):
        proposals: DefaultDict[Point2D, List[Point2D]] = defaultdict(list)

        for elf in (loc for loc, val in grove.map.items() if val == "#"):

            if grove.surroundings_empty(elf):
                # print(f"Elf {elf} early out, was empty")
                continue
            this_moves = deque(moves)
            this_moves.rotate(-round)
            for move in this_moves:
                if grove.test_move(elf, move):
                    # print(f"Elf {elf} proposes move [{move}]")
                    proposals[tuple2_add(elf, grove.direction_map[move])].append(elf)
                    break
        # all moves proposed
        for new_space, elves in proposals.items():
            # any space that had only one person who wanted it can go
            if len(elves) == 1:
                # print(f"Elf {elves[0]} -> {new_space}")
                grove.map[new_space] = "#"
                grove.map[elves[0]] = "."
            else:
                pass
                # print(f"Collision at {new_space}, nobody goes there")

        print()
        grove.render()
    print(f"Final bounding box: {grove.get_bounding_box()}")
    # count the number of empty squares inside the bounding box?
    (min, max) = grove.get_bounding_box()
    result = sum(
        1 if grove.test_empty((x, y)) else 0
        for x in range(min[0], max[0] + 1)
        for y in range(min[1], max[1] + 1)
    )
    return result


def part_two(lines) -> int:
    grove = parse_lines(lines)
    grove.render()
    moves = ["n", "s", "w", "e"]

    for round in itertools.count(start=0, step=1):
        round_moved = False
        proposals: DefaultDict[Point2D, List[Point2D]] = defaultdict(list)

        for elf in (loc for loc, val in grove.map.items() if val == "#"):

            if grove.surroundings_empty(elf):
                continue
            this_moves = deque(moves)
            this_moves.rotate(-round)
            for move in this_moves:
                if grove.test_move(elf, move):
                    proposals[tuple2_add(elf, grove.direction_map[move])].append(elf)
                    break
        for new_space, elves in proposals.items():
            if len(elves) == 1:
                grove.map[new_space] = "#"
                grove.map[elves[0]] = "."
                round_moved = True
            else:
                pass

        if round % 10 == 1:
            print()
            grove.render()
        if not round_moved:
            # the puzzle is 1-indexed
            return round + 1
    raise AssertionError("unreachable")


def main() -> None:
    with open("day23_input.txt", "r") as file:
        lines = file.read().splitlines()
        print(part_one(lines))
        print(part_two(lines))


if __name__ == "__main__":
    main()
