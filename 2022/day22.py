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


def tuple2_mul(a: Point2D, b: Point2D) -> Point2D:
    return (a[0] * b[0], a[1] * b[1])
    # return tuple([b * x for x in a])  # type: ignore


class PacmanMap:
    map: dict[Point2D, str]

    step_map: dict[Point2D, str]
    moves: List[str]

    facings = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    step_marks = [">", "V", "<", "^"]

    facing_index = 0
    facing = facings[facing_index]

    cube_edge_size: int = 0

    loc: Point2D

    def __init__(self):
        self.map = {}
        self.step_map = {}

    def _update_map(self):
        self.step_map[self.loc] = self.step_marks[self.facing_index]

    def _rotate_to_index(self, idx: int) -> None:
        self.facing_index = idx
        self.facing = self.facings[idx]
        # update map since we look different now
        self._update_map()

    def _rotate_to_facing(self, facing: Point2D) -> None:
        idx = self.facings.index(facing)
        self._rotate_to_index(idx)

    def _rotate(self, turns: int) -> None:
        self._rotate_to_index((self.facing_index + turns) % len(self.facings))

    def turn_left(self) -> None:
        self._rotate(-1)

    def turn_right(self) -> None:
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

    def step_to(self, new_loc: Point2D) -> None:
        self.loc = new_loc
        self._update_map()

    def render_quadrants(self) -> None:
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
                buffer += str(self.get_quadrant(pt))
            print(buffer)

    def fifty_cube_transitions(self) -> None:
        match (self.get_quadrant(self.loc), self.facing):
            # D
            case (1, (-1, 0)):
                self.stutter_step(4, (1, 0))
            case (4, (-1, 0)):
                self.stutter_step(1, (1, 0))
            # F
            case (6, (0, 1)):
                self.stutter_step(2, (0, 1))
            case (2, (0, -1)):
                self.stutter_step(6, (0, -1))

            # G
            case (2, (1, 0)):
                self.stutter_step(5, (-1, 0))
            case (5, (1, 0)):
                self.stutter_step(2, (-1, 0))

            # A
            case (5, (0, 1)):
                self.stutter_step(6, (-1, 0))
            case (6, (1, 0)):
                self.stutter_step(5, (0, -1))

            # C
            case (2, (0, 1)):
                self.stutter_step(3, (-1, 0))
            case (3, (1, 0)):
                self.stutter_step(2, (0, -1))

            # E
            case (6, (-1, 0)):
                self.stutter_step(1, (0, 1))
            case (1, (0, -1)):
                self.stutter_step(6, (1, 0))

            # B
            case (3, (-1, 0)):
                self.stutter_step(4, (0, 1))
            case (4, (0, -1)):
                self.stutter_step(3, (1, 0))

            case _:
                raise AssertionError(
                    f"Don't know what to do from quadrant {self.get_quadrant(self.loc)} and facing {self.facing}"
                )

    def four_cube_transitions(self) -> None:
        match (self.get_quadrant(self.loc), self.facing):

            # A
            case (4, (1, 0)):
                self.stutter_step(6, (0, 1))
            case (6, (0, -1)):
                self.stutter_step(4, (-1, 0))

            # F
            case (5, (0, 1)):
                self.stutter_step(2, (0, -1))
            case (2, (0, 1)):
                self.stutter_step(5, (0, -1))

            # B
            case (3, (0, -1)):
                self.stutter_step(1, (1, 0))
            case (1, (-1, 0)):
                self.stutter_step(3, (0, 1))

            case (1, (1, 0)):
                self.stutter_step(6, (-1, 0))
            case (6, (1, 0)):
                self.stutter_step(1, (-1, 0))

            case _:
                raise AssertionError(
                    f"Don't know what to do from quadrant {self.get_quadrant(self.loc)} and facing {self.facing}"
                )

    def step_one_cube_rules(self) -> None:
        old_loc = self.loc
        next_loc = tuple2_add(self.facing, self.loc)

        # base case: we made it
        if not self.test_in_space(next_loc):
            if self.test_empty(next_loc):
                self.step_to(next_loc)
                print(f"step {next_loc}")
                return
            else:
                # bumped
                return

        if self.cube_edge_size == 4:
            self.four_cube_transitions()
        elif self.cube_edge_size == 50:
            self.fifty_cube_transitions()
        else:
            assert False

    def stutter_step(
        self,
        side: int,
        new_facing: Point2D,
    ) -> None:
        # offset dir is always abs(swap(new_facing)
        offset_dir = (abs(new_facing[1]), abs(new_facing[0]))
        # offset (scalar) is always offset_dir * loc
        offset_scalar = self.loc[1] if self.facing[1] == 0 else self.loc[0]
        offset_scalar = offset_scalar % self.cube_edge_size
        # we twist if direction change xor polarity change
        rotated = (self.facing[0] == 0) == (new_facing[1] == 0)
        flipped = sum(self.facing) != sum(new_facing)
        twist = flipped ^ rotated
        if twist:
            offset_scalar = (self.cube_edge_size - 1) - offset_scalar

        offset_vector = tuple2_scalar_mul(offset_dir, offset_scalar)
        corner_real = tuple2_scalar_mul(
            self.side_to_corner()[side], self.cube_edge_size
        )
        next_loc = tuple2_add(offset_vector, corner_real)
        if new_facing[1] == -1:
            # move to the bottom side
            next_loc = tuple2_add(next_loc, (0, self.cube_edge_size - 1))
        elif new_facing[0] == -1:
            # move to the right side
            next_loc = tuple2_add(next_loc, (self.cube_edge_size - 1, 0))

        assert next_loc in self.map
        if self.test_empty(next_loc):
            self.step_to(next_loc)
            self._rotate_to_facing(new_facing)

    def step_one_pacman_rules(self) -> None:
        old_loc = self.loc
        next_loc = tuple2_add(self.facing, self.loc)

        # base case: we made it
        if not self.test_in_space(next_loc):
            if self.test_empty(next_loc):
                self.step_to(next_loc)
                # print(f"step {next_loc}")
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
            self.step_to(next_loc)
            # print(f"Wrapped around to {next_loc}")
        else:
            # bumped
            return

        return

    def corner_to_side(self) -> Dict[Point2D, int]:

        return {
            4: {
                (2, 0): 1,
                (0, 1): 2,
                (1, 1): 3,
                (2, 1): 4,
                (2, 2): 5,
                (3, 2): 6,
            },
            50: {
                (1, 0): 1,
                (2, 0): 2,
                (1, 1): 3,
                (0, 2): 4,
                (1, 2): 5,
                (0, 3): 6,
            },
        }[self.cube_edge_size]

    def side_to_corner(self) -> Dict[int, Point2D]:

        return {v: k for k, v in self.corner_to_side().items()}

    def get_quadrant(self, loc: Point2D) -> int:
        if not loc in self.map:
            return 0

        cube_side = (loc[0] // self.cube_edge_size, loc[1] // self.cube_edge_size)
        if side := self.corner_to_side().get(cube_side):
            return side

        raise AssertionError(
            f"Couldn't place {loc} with cube size {self.cube_edge_size}"
        )

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
            if pac.cube_edge_size == 0:
                pac.cube_edge_size = len(line) // 3

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
                    pac.step_one_pacman_rules()

    # The final password is the sum of 1000 times the row, 4 times the column, and the facing.
    print(
        f"Final loc: {pac.loc} and facing {pac.facing} and facing index {pac.facings.index(pac.facing)}"
    )
    pac.render()
    return (
        1000 * (pac.loc[1] + 1) + 4 * (pac.loc[0] + 1) + pac.facings.index(pac.facing)
    )


def part_two(lines) -> int:
    pac = parse_lines(lines)
    # pac.render()
    # pac.render_quadrants()
    # return 0

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
                    pac.step_one_cube_rules()

    # The final password is the sum of 1000 times the row, 4 times the column, and the facing.
    print(
        f"Final loc: {pac.loc} and facing {pac.facing} and facing index {pac.facings.index(pac.facing)}"
    )
    pac.render()
    return (
        1000 * (pac.loc[1] + 1) + 4 * (pac.loc[0] + 1) + pac.facings.index(pac.facing)
    )

    return 0


def main() -> None:
    with open("day22_input.txt", "r") as file:
        lines = file.read().splitlines()
        print(part_one(lines))
        print(part_two(lines))


if __name__ == "__main__":
    main()
