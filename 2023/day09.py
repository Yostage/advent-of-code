import functools
import itertools
import re
from dataclasses import dataclass, field
from functools import cache
from typing import Any, Dict, List, TypeVar


def parse_lines(lines: List[str]) -> Any:
    return [[int(s) for s in line.split(" ")] for line in lines]


def predict_next(history: List[int]) -> int:
    level_history: List[List[int]] = []
    this_level = history

    while not all(x == 0 for x in this_level):
        level_history.append(this_level)
        this_level = [b - a for (a, b) in itertools.pairwise(this_level)]

    # now go back up
    for lower, higher in itertools.pairwise(reversed(level_history)):
        higher.append(higher[-1] + lower[-1])

    # print(level_history)
    return level_history[0][-1]


def predict_prev(history: List[int]) -> int:
    level_history: List[List[int]] = []
    this_level = history

    while not all(x == 0 for x in this_level):
        level_history.append(this_level)
        this_level = [b - a for (a, b) in itertools.pairwise(this_level)]
    # print(level_history)
    # now go back up
    for lower, higher in itertools.pairwise(reversed(level_history)):
        higher.insert(0, higher[0] - lower[0])

    # print(level_history)
    return level_history[0][0]


def part_one(lines) -> int:
    histories = parse_lines(lines)
    return sum(predict_next(history) for history in histories)


def part_two(lines) -> int:
    histories = parse_lines(lines)
    return sum(predict_prev(history) for history in histories)


def main() -> None:
    with open("day09_input.txt", "r") as file:
        lines = file.read().splitlines()
        print(part_one(lines))
        print(part_two(lines))


if __name__ == "__main__":
    main()
