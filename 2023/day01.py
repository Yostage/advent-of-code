import functools
import re
from dataclasses import dataclass, field
from functools import cache
from typing import Any, Dict, List, TypeVar


def parse_lines(lines: List[str]) -> List[str]:
    return lines


def part_one(lines) -> int:
    lines = parse_lines(lines)
    sum = 0
    for line in lines:
        first_digit = next(filter(lambda c: c.isdigit(), line))
        last_digit = next(filter(lambda c: c.isdigit(), reversed(line)))
        sum += 10 * int(first_digit) + int(last_digit)

    return sum


welp = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}


def part_two(lines) -> int:
    def downshift(c: str) -> int:
        if c.isdigit():
            return int(c)
        return welp[c]

    lines = parse_lines(lines)
    sum = 0
    pattern = r"\d" + "|" + "one|two|three|four|five|six|seven|eight|nine"
    reversed_pattern = "\d" + "|" + "one|two|three|four|five|six|seven|eight|nine"[::-1]
    for line in lines:
        digits = re.findall(pattern, line)
        sum += 10 * downshift(digits[0])
        digits = re.findall(reversed_pattern, line[::-1])
        sum += downshift(digits[0][::-1])
        # print(f"input: [{line}] -> [{digits[0]}], [{digits[-1]}]")

    return sum


def main() -> None:
    with open("day01_input.txt", "r") as file:
        lines = file.read().splitlines()
        print(part_one(lines))
        print(part_two(lines))


if __name__ == "__main__":
    main()
