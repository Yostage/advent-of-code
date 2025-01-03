import functools
import re
from dataclasses import dataclass, field
from functools import cache
from typing import Any, Deque, Dict, List, Set, Tuple, TypeVar


def parse_lines(lines: List[str]) -> List[str]:
    return lines[0].split(" ")


def evolve(stones: List[str]) -> List[str]:
    ret = []
    for stone in stones:
        if stone == "0":
            ret.append("1")
        elif len(stone) % 2 == 0:
            ret.append(str(int(stone[0 : len(stone) // 2])))
            ret.append(str(int(stone[len(stone) // 2 :])))
        else:
            ret.append(str(int(stone) * 2024))
    return ret


def part_one(lines) -> int:
    stones = parse_lines(lines)
    for _ in range(25):
        # for _ in range(6):
        stones = evolve(stones)
        # print(f"{_+1} : {stones}")

    return len(stones)


def part_two(lines) -> int:
    parse_lines(lines)
    return 0


def main() -> None:
    with open("day11_input.txt", "r") as file:
        lines = file.read().splitlines()
        print(part_one(lines))
        print(part_two(lines))


if __name__ == "__main__":
    main()
