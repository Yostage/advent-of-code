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

    def __hash__(self):
        return hash((self.x, self.y))


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
    return 0 if x == 0 else copysign(1, x)


class SnakeGame:
    head = Point(0, 0)
    tail = Point(0, 0)

    def move_head(self, move: Move) -> None:
        for _ in range(move.magnitude):
            self.head = self.move_point(self.head, move.dir)
            self.update_tail()

    def update_tail(self) -> None:
        # tail is one or zero spaces away, stay put
        # if abs(self.head.x - self.tail.x)  2 and abs(self.head.y - self.tail.y) < 2:
        # return
        # otherwise, move tail at most one spaces on both x and y
        delta_x = self.head.x - self.tail.x
        delta_y = self.head.y - self.tail.y
        if abs(delta_x) < 2 and abs(delta_y) < 2:
            return

        self.tail.x += sign(delta_x)
        self.tail.y += sign(delta_y)

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
    snake = SnakeGame()
    tail_positions = set()
    for move in moves:
        for _ in range(move.magnitude):
            snake.head = snake.move_point(snake.head, move.dir)
            snake.update_tail()
            # print(
            #     f"head = [{snake.head.x}, {snake.head.y}, tail = [{snake.tail.x}, {snake.tail.y}]"
            # )
            tail_positions.add((snake.tail.x, snake.tail.y))

        # snake.move_head(move)

    # print(tail_positions)
    # for y in range(5):
    #     print("".join(["X" if (x, y) in tail_positions else "." for x in range(5)]))

    return len(tail_positions)


def part_two(lines):
    parse_lines(lines)
    return None


def main():
    with open("day9_input.txt", "r") as file:
        lines = file.read().splitlines()
        print(part_one(lines))
        print(part_two(lines))


if __name__ == "__main__":
    main()
