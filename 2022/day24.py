import functools
import re
from collections import defaultdict
from dataclasses import dataclass, field
from functools import cache
from itertools import count
from typing import Any, DefaultDict, Dict, List, Set, TypeVar

from day15 import Point2D
from day22 import tuple2_add


class BlizzardMap:
    map: DefaultDict[Point2D, str]
    wall_up = 0
    wall_left = 0
    wall_right = 8
    wall_down = 10
    loc: Point2D = (1, 0)

    blizzards: Dict[Point2D, List[str]]

    reachable: Set[Point2D]

    def __init__(self):
        self.map = defaultdict(lambda: ".")
        self.blizzards = defaultdict(list)
        self.reachable = set()
        self.reachable.add((1, 0))

    def move_blizzards(self) -> None:
        def respawn_point(bliz: str, pos: Point2D) -> Point2D:
            match bliz:
                case ">":
                    return (self.wall_left + 1, pos[1])
                case "<":
                    return (self.wall_right - 1, pos[1])
                case "^":
                    return (pos[0], self.wall_down - 1)
                case "v":
                    return (pos[0], self.wall_up + 1)
                case _:
                    raise AssertionError(f"unknown bliz {bliz}")

        blizzard_moves = {
            ">": (1, 0),
            "<": (-1, 0),
            "^": (0, -1),
            "v": (0, 1),
        }

        tomorrow_blizzards: Dict[Point2D, List[str]] = defaultdict(list)
        for spot, blizzards in self.blizzards.items():
            for blizzard in blizzards:
                new_space = tuple2_add(spot, blizzard_moves[blizzard])
                # move if we're open
                if self.blizzard_safe_space(new_space):
                    tomorrow_blizzards[new_space].append(blizzard)
                else:
                    # regenerate if we're not
                    tomorrow_blizzards[respawn_point(blizzard, new_space)].append(
                        blizzard
                    )
        self.blizzards = tomorrow_blizzards

    def advance_reachable(self) -> None:
        moves = {(1, 0), (0, 1), (0, 0), (-1, 0), (0, -1)}
        tomorrow_reachable = set()
        for r in self.reachable:
            for move in moves:
                test = tuple2_add(r, move)
                if self.test_empty(test):
                    tomorrow_reachable.add(test)
        self.reachable = tomorrow_reachable

    def blizzard_safe_space(self, loc: Point2D) -> bool:
        # hardcoded walls
        if loc[0] in (self.wall_left, self.wall_right) or loc[1] in (
            self.wall_up,
            self.wall_down,
        ):
            return False

        return True

    def test_empty(self, loc: Point2D) -> bool:

        # hack: don't let us walk back out the top
        if loc[1] < 0:
            return False

        # another hack, the doorway is open
        if loc == (1, 0):
            return True
        # hardcoded walls
        if loc[0] in (self.wall_left, self.wall_right) or loc[1] in (
            self.wall_up,
            self.wall_down,
        ):
            return False

        if loc in self.blizzards:
            return False

        return True

    def render(self) -> None:
        def char_at_square(pos: Point2D) -> str:
            if pos in self.blizzards:
                bliz = self.blizzards[pos]
                return bliz[0] if len(bliz) == 1 else str(len(bliz))

            if pos in self.reachable:
                return "*"

            if self.test_empty(pos):
                return "."
            assert False

        # first square
        print()
        print("#." + ("#" * (self.wall_right - 1)))
        for y in range(self.wall_up + 1, self.wall_down):
            print(
                "#"
                + "".join(
                    char_at_square((x, y))
                    for x in range(self.wall_left + 1, self.wall_right)
                )
                + "#"
            )
        print(("#" * (self.wall_right - 1)) + ".#")


def parse_lines(lines: List[str]) -> BlizzardMap:
    b = BlizzardMap()
    b.wall_left = 0
    b.wall_up = 0
    # ignore walls, count the content
    b.wall_right = len(lines[0]) - 1
    b.wall_down = len(lines) - 1
    # print(f"Walls at {b.wall_left, b.wall_up} -> {b.wall_right, b.wall_down}")
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char in ["v", "<", ">", "^"]:
                # print(f"Blizzard at {(x,y)}")
                b.blizzards[(x, y)].append(char)
    return b


def part_one(lines) -> int:
    b = parse_lines(lines)
    b.render()
    for round in count(1):
        b.move_blizzards()
        b.advance_reachable()
        if round % 10 == 1:
            b.render()
        # if we run out of spaces we're dead forever
        assert len(b.reachable) > 0
        if (b.wall_right - 1, b.wall_down - 1) in b.reachable:
            # it would take one more round to walk out
            return round + 1

    return 0


def part_two(lines) -> int:
    parse_lines(lines)
    return 0


def main() -> None:
    with open("day24_input.txt", "r") as file:
        lines = file.read().splitlines()
        print(part_one(lines))
        print(part_two(lines))


if __name__ == "__main__":
    main()
