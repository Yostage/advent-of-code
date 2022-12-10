import functools
import re
from dataclasses import dataclass, field
from functools import cache
from typing import Any, Dict, List, TypeVar


def parse_lines(lines: List[str]) -> Any:
    return lines


def part_one(lines):
    input = parse_lines(lines)
    cycle = 0
    x_register = 1
    interesting_signals = []

    def check_clock():
        if cycle % 40 == 20:
            print(f"registering signal @ {cycle} = {cycle * x_register}")
            interesting_signals.append(cycle * x_register)

    for line in input:
        # process instruction
        if line == "noop":
            cycle += 1
            check_clock()
        elif line.startswith("addx"):
            (_, param) = line.split(" ")
            cycle += 1
            check_clock()
            cycle += 1
            check_clock()
            x_register += int(param)
        else:
            print(f"parse error [{line}]")
            assert False
        # check signal strengths
        # print(f"clock cycle = {cycle} x = {x_register}")
        # check_clock()

    return sum(interesting_signals)


def part_two(lines):
    parse_lines(lines)
    return None


def main():
    with open("day10_input.txt", "r") as file:
        lines = file.read().splitlines()
        print(part_one(lines))
        print(part_two(lines))


if __name__ == "__main__":
    main()
