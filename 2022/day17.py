import functools
import itertools
import re
from collections import defaultdict
from dataclasses import dataclass, field
from functools import cache
from typing import Any, Dict, Iterable, List, TypeVar

from day15 import Point2D

# X goes right. Y goes UP
# (0,0) is the bottom left wall


class Tetris:
    map: defaultdict[Point2D, str]
    top_rock = 0
    wall_left = 0
    wall_right = 8
    floor = 0

    def __init__(self):
        self.map = defaultdict(lambda: ".")

    def test_empty(self, loc: Point2D) -> bool:
        # hardcoded walls
        if (
            loc[0] == self.wall_left
            or loc[0] == self.wall_right
            or loc[1] == self.floor
        ):
            return False

        if not loc in self.map:
            return True
        # avoid overpopulating the map
        return self.map[loc] == "."


class Rock:
    # offsets from locus
    _pixel_offsets: List[Point2D]
    # the bottom left point, which may not be a pixel
    locus: Point2D

    def __init__(self, bottom_left: Point2D, template_index: int):
        self.locus = bottom_left
        self._pixel_offsets = Rock._rock_template(template_index)

    def apply(self, offset: Point2D) -> None:
        self.locus = tuple(map(sum, zip(self.locus, offset)))  # type: ignore

    def all_pixels(self) -> Iterable[Point2D]:
        return (
            (px[0] + self.locus[0], px[1] + self.locus[1]) for px in self._pixel_offsets
        )

    # test whether the offset space is safe
    def test_all_empty(self, tet: Tetris, offset: Point2D):
        # todo
        for px in self.all_pixels():
            testing_loc = tuple(map(sum, zip(px, offset)))  # type: ignore

            if not tet.test_empty(testing_loc):  # type: ignore
                return False
        return True
        # i'm not smart enough merry christmas
        # offsets = [list(map(sum, zip(self.locus, offset, px))) for px in self.pixels]
        # return all([tet.test_empty(px2) for px2 in offsets])

    @staticmethod
    def _rock_template(index: int) -> List[Point2D]:
        match index:
            case 0:
                # ----
                return [(0, 0), (1, 0), (2, 0), (3, 0)]

            case 1:
                # +
                return [(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)]
            case 2:
                # ___|
                return [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)]
            case 3:
                # |
                return [(0, 0), (0, 1), (0, 2), (0, 3)]

            case 4:
                # box
                return [(0, 0), (0, 1), (1, 0), (1, 1)]
            case other:
                raise AssertionError(f"{index} unknown rock template")


def parse_lines(lines: List[str]) -> List[str]:
    assert len(lines) == 1
    return list(lines[0])


def render(tet: Tetris) -> None:
    print()
    for y in range(tet.top_rock, 0, -1):
        line = (
            ["|"]
            + [tet.map[x, y] for x in range(tet.wall_left + 1, tet.wall_right)]
            + ["|"]
        )
        print("".join(line))
    print("---------")
    print()


def part_one(lines: List[str], count_rocks: int = 2022) -> int:
    jet_sequence = parse_lines(lines)

    jets = itertools.cycle(jet_sequence)
    rock_indexes = itertools.cycle(range(0, 5))
    offsets = {">": (1, 0), "<": (-1, 0)}

    tet = Tetris()
    rocks_dropped = 0
    for _ in range(count_rocks):
        rock_index = next(rock_indexes)
        r = Rock((3, tet.top_rock + 4), rock_index)

        while True:
            offset = offsets[next(jets)]
            if r.test_all_empty(tet, offset):
                r.apply(offset)
            # assert r.test_all_empty(tet, (0, 0))

            down_vec = (0, -1)
            # if drop safe, apply drop

            if r.test_all_empty(tet, down_vec):
                r.apply(down_vec)
                # assert r.test_all_empty(tet, (0, 0))
            else:

                # assert r.test_all_empty(tet, (0, 0))
                for px in r.all_pixels():
                    # turn to stone where you are
                    tet.map[px] = "#"
                    # print(f"Writing {px} into map")

                    # and update max height
                    tet.top_rock = max(px[1], tet.top_rock)
                # and stop
                break

    # after 2022 rocks have fallen. what's the tallest space?
    # render(tet)
    return tet.top_rock


def part_two(lines) -> int:
    parse_lines(lines)
    return 0


def main() -> None:
    with open("day17_input.txt", "r") as file:
        lines = file.read().splitlines()
        print(part_one(lines))
        print(part_two(lines))


if __name__ == "__main__":
    main()
