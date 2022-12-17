import functools
import re
from dataclasses import dataclass, field
from functools import cache
from itertools import zip_longest
from math import copysign
from typing import Any, Dict, List, TypeVar

from more_itertools import grouper, quantify


def sign(x: int) -> int:
    return 0 if x == 0 else int(copysign(1, x))


# def compare(left: Union[List|int], right:Union[List|int])
def compare(left: List | int, right: List | int) -> int:
    if isinstance(left, int) and isinstance(right, int):
        # return left < right
        return sign(left - right)
    elif isinstance(left, List) and isinstance(right, List):
        for pair in zip(left, right):
            pairwise = compare(pair[0], pair[1])
            if pairwise != 0:
                return pairwise

        # left list should be shorter
        # every entry in list should be
        return compare(len(left), len(right))
    else:
        return False


def parse_lines(lines: List[str]) -> Any:
    return [
        (eval(pair[0]), eval(pair[1]))
        for pair in grouper(filter(lambda l: len(l) > 0, lines), 2)
    ]


def part_one(lines) -> int:
    pairs = parse_lines(lines)
    results = [compare(left, right) for left, right in pairs]
    total = 1
    print(results)
    for idx, result in enumerate(results):
        if result != 1:
            total *= idx + 1
    return total
    # return quantify(results, lambda x: x == -1)


def part_two(lines) -> int:
    parse_lines(lines)
    return 0


def main() -> None:
    with open("day13_input.txt", "r") as file:
        lines = file.read().splitlines()
        print(part_one(lines))
        print(part_two(lines))


if __name__ == "__main__":
    main()
