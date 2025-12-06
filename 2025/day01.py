import functools
import re
from dataclasses import dataclass, field
from functools import cache
from typing import Any, Deque, Dict, List, Set, Tuple, TypeVar


def parse_lines(lines: List[str]) -> Any:
    return [(line[0], int(line[1:])) for line in lines]


def part_one(lines) -> int:
    dial = 50
    clicks = 0
    turns = parse_lines(lines)
    for turn in turns:
        direction, distance = turn
        if direction == "L":
            dial -= distance
        else:
            dial += distance
        dial %= 100
        if dial == 0:
            clicks += 1

    return clicks


def part_two_impl(dial, distance) -> Tuple[int, int]:

    # take all the extra hundreds out of the distance
    clicks = abs(distance) // 100
    one_spin = distance % 100

    new_dial = (dial + one_spin) % 100

    if dial == 0:
        return new_dial, clicks

    # landed on 0
    if new_dial == 0:
        clicks += 1
    # passed over it
    elif distance > 0 and new_dial < dial:
        clicks += 1
    elif distance < 0 and new_dial > dial:
        clicks += 1

    return new_dial, clicks


def part_two(lines) -> int:
    dial = 50
    clicks = 0
    turns = parse_lines(lines)

    for turn in turns:

        # print(f"Dial: {dial}. Clicks: {clicks}")
        # print(turn)
        direction, distance = turn
        assert distance != 0
        if direction == "L":
            distance *= -1

        dial, new_clicks = part_two_impl(dial, distance)
        clicks += new_clicks
        # print()

    return clicks


def main() -> None:
    with open("day01_input.txt", "r") as file:
        lines = file.read().splitlines()
        print(part_one(lines))
        print(part_two(lines))


if __name__ == "__main__":
    main()
