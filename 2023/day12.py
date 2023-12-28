import functools
import re
from dataclasses import dataclass, field
from functools import cache
from typing import Any, Dict, List, Tuple, TypeVar


def parse_lines(lines: List[str]) -> List[Tuple[str, List[int]]]:
    ret = []
    for line in lines:
        (springs, seg_string) = line.split(" ")
        segments = [int(s) for s in seg_string.split(",")]
        ret.append((springs, segments))
    return ret


def how_many_legal(springs, segments) -> int:
    return 7


def part_one(lines) -> int:
    data = parse_lines(lines)
    sum = 0
    for springs, segments in data:
        answer = how_many_legal(springs, segments)
        print(
            f"{springs} : {','.join([str(s) for s in segments])} : {how_many_legal(springs, segments)}"
        )
        sum += answer

    return sum


def part_two(lines) -> int:
    parse_lines(lines)
    return 0


def main() -> None:
    with open("day12_input.txt", "r") as file:
        lines = file.read().splitlines()
        print(part_one(lines))
        print(part_two(lines))


if __name__ == "__main__":
    main()
