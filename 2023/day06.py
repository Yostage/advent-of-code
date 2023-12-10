import functools
import math
import re
from dataclasses import dataclass, field
from functools import cache
from typing import Any, Dict, List, Tuple, TypeVar


def parse_lines(lines: List[str]) -> List[Tuple[int, int]]:
    # for line in lines:
    #     # (_, the_rest) = line.split(":")
    times = [int(s) for s in re.findall("\d+", lines[0])]
    distances = [int(d) for d in re.findall("\d+", lines[1])]
    return list(zip(times, distances))
    # print(nums)
    # return None


def part_one(lines) -> int:
    races = parse_lines(lines)
    winning_options = []
    for race in races:
        wins = 0
        (time, distance) = race
        for time_held in range(time):
            if time_held * (time - time_held) > distance:
                wins += 1
        winning_options.append(wins)

    return math.prod(winning_options)


def part_two(lines) -> int:
    races = parse_lines(lines)
    # oops all kerning
    time = int("".join([str(r[0]) for r in races]))
    distance = int("".join([str(r[1]) for r in races]))
    wins = 0
    # i think we could binary search this?
    for time_held in range(time):
        if time_held * (time - time_held) > distance:
            wins += 1
    return wins


def main() -> None:
    with open("day06_input.txt", "r") as file:
        lines = file.read().splitlines()
        print(part_one(lines))
        print(part_two(lines))


if __name__ == "__main__":
    main()
