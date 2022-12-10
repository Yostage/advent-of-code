from functools import cache
import functools
import re
from typing import Any, Dict, List


from dataclasses import dataclass, field
from typing import TypeVar


@dataclass
class Point:
    x: int
    y: int


@dataclass
class Move:
    dir: str
    magnitude: int

    def __str__(self):
        return f"{self.dir} {self.magnitude}"

    def __repr__(self):
        return f"{self.dir} {self.magnitude}"


supported_directions = ["L", "R", "U", "D", "UL", "UR", "DL", "DR"]

from math import copysign


def sign(x: int) -> int:
    return 0 if x == 0 else int(copysign(1, x))


class SnakeGame:
    segments: List[Point]

    def __init__(self, length: int):
        self.segments = [Point(0, 0) for _ in range(length)]

    def one_step(self, dir: str) -> None:
        # the head moves
        self.segments[0] = self.move_point(self.segments[0], dir)
        # every single segment then possibly updates afterwards
        for idx in range(1, len(self.segments)):
            self.segments[idx] = self.update_segment(
                self.segments[idx], self.segments[idx - 1]
            )

    def update_segment(self, tail: Point, head: Point) -> Point:
        delta_x = head.x - tail.x
        delta_y = head.y - tail.y

        # tail is one or zero spaces away, stay put
        if abs(delta_x) < 2 and abs(delta_y) < 2:
            return tail

        # otherwise, move tail at most one spaces on both x and y
        return Point(tail.x + sign(delta_x), tail.y + sign(delta_y))

    def move_point(self, input: Point, direction: str) -> Point:
        assert direction in supported_directions
        match direction:
            case "L":
                return Point(input.x - 1, input.y)
            case "R":
                return Point(input.x + 1, input.y)
            case "U":
                return Point(input.x, input.y + 1)
            case "D":
                return Point(input.x, input.y - 1)
            case "UL":
                return Point(input.x - 1, input.y + 1)
            case "UR":
                return Point(input.x + 1, input.y + 1)
            case "DL":
                return Point(input.x - 1, input.y - 1)
            case "DR":
                return Point(input.x + 1, input.y - 1)
            case _:
                assert False


def parse_lines(lines: List[str]) -> List[Move]:
    results = []
    for line in lines:
        (dir, magnitude) = line.split(" ")
        results.append(Move(dir, int(magnitude)))
    assert dir in supported_directions
    return results


def part_one(lines):
    moves = parse_lines(lines)
    snake = SnakeGame(2)
    tail_positions = set()
    for move in moves:
        for _ in range(move.magnitude):
            snake.one_step(move.dir)
            tail_positions.add((snake.segments[1].x, snake.segments[1].y))

    # print(tail_positions)
    # for y in range(5):
    #     print("".join(["X" if (x, y) in tail_positions else "." for x in range(5)]))

    return len(tail_positions)


def part_two(lines):
    moves = parse_lines(lines)
    snake = SnakeGame(10)
    tail_positions = set()
    for move in moves:
        for _ in range(move.magnitude):
            snake.one_step(move.dir)
            tail_positions.add((snake.segments[9].x, snake.segments[9].y))

    return len(tail_positions)


def main():
    with open("day9_input.txt", "r") as file:
        lines = file.read().splitlines()
        print(part_one(lines))
        print(part_two(lines))


if __name__ == "__main__":
    main()
