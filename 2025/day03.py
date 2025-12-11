import functools
import re
from dataclasses import dataclass, field
from functools import cache
from typing import Any, Deque, Dict, List, Set, Tuple, TypeVar


def parse_lines(lines: List[str]) -> Any:
    return lines


def part_one(lines) -> int:
    parse_lines(lines)
    total = 0
    for line in lines:
        batteries = [int(x) for x in line]
        tens_place = max(batteries[:-1])
        first_battery = batteries.index(tens_place)
        the_rest = batteries[first_battery + 1 :]
        ones_place = max(the_rest)
        total += 10 * tens_place + ones_place
    return total


def part_two(lines) -> int:
    parse_lines(lines)
    batteries_per_line = 12
    total = 0
    for line in lines:
        print(line)
        first_available = 0
        batteries = [int(x) for x in line]

        lit = []
        for slot in range(batteries_per_line):
            # first one should be 0:-11
            # print("currently lit", lit)
            last_available = -(batteries_per_line - 1 - slot)
            if last_available == 0:
                last_available = None
            # print("RANGE", first_available, last_available)
            slice = batteries[first_available:last_available]
            # print("Batteries", slice)
            this_place = max(slice)
            lit.append(this_place)
            first_available = first_available + slice.index(this_place) + 1
            # print("Chose battery at index ", first_available - 1)

        this_line = 0
        for l in lit:
            this_line *= 10
            this_line += l

        # print("This line", this_line)
        total += this_line
    return total


def main() -> None:
    with open("day03_input.txt", "r") as file:
        lines = file.read().splitlines()
        print(part_one(lines))
        print(part_two(lines))


if __name__ == "__main__":
    main()
