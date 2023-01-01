import functools
import itertools
import re
from dataclasses import dataclass, field
from functools import cache
from typing import Any, Dict, List, TypeVar

from day15 import Point2D


def tuple2_add(a: Point2D, b: Point2D) -> Point2D:
    return tuple(map(sum, zip(a, b)))  # type: ignore


def tuple2_scalar_mul(a: Point2D, b: int) -> Point2D:
    return tuple([b * x for x in a])  # type: ignore


class PacmanMap:
    map: dict[Point2D, str]

    step_map: dict[Point2D, str]
    moves: List[str]

    facings = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    step_marks = [">", "V", "<", "^"]

    facing_index = 0
    facing = facings[facing_index]

    loc: Point2D

    def __init__(self):
        self.map = {}
        self.step_map = {}

    def _rotate(self, turns: int):
        self.facing_index = (self.facing_index + turns) % len(self.facings)
        self.facing = self.facings[self.facing_index]

    def turn_left(self):
        self._rotate(-1)

    def turn_right(self):
        self._rotate(1)

    def get_one_row(self, y: int) -> List[Point2D]:
        return list(sorted(p for p in self.map if p[1] == y))

    def render(self) -> None:
        by_y = itertools.groupby(
            sorted(self.map, key=lambda p: p[1]), key=lambda p: p[1]
        )
        for _, row in by_y:
            px = list(row)
            buffer = ""
            for idx, pt in enumerate(sorted(px)):
                # print as many spaces as are missing
                if idx == 0:
                    buffer = " " * pt[0]
                buffer += self.step_map[pt] if pt in self.step_map else self.map[pt]
            print(buffer)

    def step_one(self) -> None:
        old_loc = self.loc
        next_loc = tuple2_add(self.facing, self.loc)

        # base case: we made it
        if not self.test_in_space(next_loc):
            if self.test_empty(next_loc):
                self.loc = next_loc
                self.step_map[old_loc] = self.step_marks[self.facing_index]
                print(f"step {next_loc}")
                return
            else:
                # bumped
                return

        # next_loc off the map right now
        # moonwalk until we hit the edge
        reverse_facing = tuple2_scalar_mul(self.facing, -1)
        # turn around
        next_loc = tuple2_add(reverse_facing, self.loc)
        # keep going until we hit the edge
        # our real facing is preserved because pacman rules
        while not self.test_in_space(next_loc):
            next_loc = tuple2_add(reverse_facing, next_loc)
        # snap back one space since we walked off the edge
        next_loc = tuple2_add(self.facing, next_loc)

        if self.test_empty(next_loc):
            self.loc = next_loc
            self.step_map[old_loc] = self.step_marks[self.facing_index]
            print(f"Wrapped around to {next_loc}")
        else:
            # bumped
            return

        return

    def test_in_space(self, loc: Point2D) -> bool:
        return not loc in self.map

    def test_empty(self, loc: Point2D) -> bool:
        if not loc in self.map:
            return True
        # avoid overpopulating the map
        return self.map[loc] == "."


def parse_lines(lines: List[str]) -> PacmanMap:
    y = 0
    pac = PacmanMap()
    parsing_map = True
    for line in lines:
        # skip the delimiter
        if len(line) == 0:
            # print("Parsing blank line")
            continue
        elif line[0].isdigit():
            # this is the moves line
            pac.moves = re.findall(r"(\d+|R|L)", line)
            continue
        else:
            # this is a map line
            for idx, s in enumerate(line):
                if s.isspace():
                    continue
                else:
                    # print(f"({idx}, {y}) = '{s}'")
                    pac.map[(idx, y)] = s
            y += 1

    return pac


def part_one(lines) -> int:
    pac = parse_lines(lines)
    pac.render()

    # we start at the most upper left space
    row_0 = pac.get_one_row(0)
    pac.loc = row_0[0]
    print(f"Starting at {pac.loc}")
    print(f"Movelist: {pac.moves}")
    for move in pac.moves:
        print(f"Move: [{move}]")
        match move:
            case "L":
                pac.turn_left()
            case "R":
                pac.turn_right()
            case _:
                for _ in range(int(move)):
                    pac.step_one()

    # The final password is the sum of 1000 times the row, 4 times the column, and the facing.
    print(
        f"Final loc: {pac.loc} and facing {pac.facing} and facing index {pac.facings.index(pac.facing)}"
    )
    pac.render()
    return (
        1000 * (pac.loc[1] + 1) + 4 * (pac.loc[0] + 1) + pac.facings.index(pac.facing)
    )


def part_two(lines) -> int:
    parse_lines(lines)
    return 0


def main() -> None:
    with open("day22_input.txt", "r") as file:
        lines = file.read().splitlines()
        print(part_one(lines))
        print(part_two(lines))


if __name__ == "__main__":
    main()
