import functools
import re
from collections import defaultdict
from dataclasses import dataclass, field
from functools import cache
from itertools import combinations, count, pairwise
from typing import Any, DefaultDict, Deque, Dict, List, Set, Tuple, TypeVar

from CharacterGrid import CharacterGrid
from util import tuple2_add, tuple2_scalar_mul, tuple2_sub


def parse_lines(lines: List[str]) -> CharacterGrid:
    return CharacterGrid.from_lines(lines)


def part_one(lines) -> int:
    map = parse_lines(lines)
    antennas = defaultdict(list)
    antinodes = set()

    # fetch all antenna into a list of locations keyed by the antenna character
    for loc, char in map.map.items():
        if char == ".":
            continue
        antennas[char].append(loc)

    # find all the antinodes
    for code, locations in antennas.items():
        for pair in combinations(locations, 2):
            slope = tuple2_sub(pair[1], pair[0])
            antinodes.add(tuple2_add(pair[1], slope))
            antinodes.add(tuple2_sub(pair[0], slope))

    # for loc in antinodes:
    #     if loc in map.map:
    #         map.map[loc] = "#"

    # map.render()

    return sum(1 for loc in antinodes if loc in map.map)

    # print(antennas)
    # return 0


def part_two(lines) -> int:
    map = parse_lines(lines)
    antennas = defaultdict(list)
    antinodes = set()

    # fetch all antenna into a list of locations keyed by the antenna character
    for loc, char in map.map.items():
        if char == ".":
            continue
        antennas[char].append(loc)

    # find all the antinodes
    for code, locations in antennas.items():
        for pair in combinations(locations, 2):
            slope = tuple2_sub(pair[1], pair[0])
            for step in count(start=0, step=1):
                loc = tuple2_add(pair[1], tuple2_scalar_mul(slope, step))
                if loc not in map.map:
                    break
                antinodes.add(loc)
            for step in count(start=-1, step=-1):
                loc = tuple2_add(pair[1], tuple2_scalar_mul(slope, step))
                if loc not in map.map:
                    break
                antinodes.add(loc)

    return sum(1 for loc in antinodes if loc in map.map)


def main() -> None:
    with open("day08_input.txt", "r") as file:
        lines = file.read().splitlines()
        print(part_one(lines))
        print(part_two(lines))


if __name__ == "__main__":
    main()
