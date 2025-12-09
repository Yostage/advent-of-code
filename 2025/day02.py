import functools
import itertools
import re
from dataclasses import dataclass, field
from functools import cache
from typing import Any, Deque, Dict, List, Set, Tuple, TypeVar


def parse_lines(lines: List[str]) -> Any:
    return lines[0].split(",")


def part_one(lines) -> int:
    total = 0
    lines = parse_lines(lines)
    for line in lines:
        (min, max) = line.split("-")
        for id in range(int(min), int(max) + 1):
            testable = str(id)
            if len(testable) % 2 != 0:
                continue
            (l, r) = (
                testable[: len(testable) // 2],
                testable[(len(testable) // 2) + len(testable) % 2 :],
            )
            if l == r:
                total += id
                print(f"Found double: {id}")
            # else:
            #     print(f"No double: {id}")

    return total


def part_two(lines) -> int:
    parse_lines(lines)
    total = 0
    lines = parse_lines(lines)
    for line in lines:
        (min, max) = line.split("-")
        for id in range(int(min), int(max) + 1):
            testable = str(id)
            for chunk_size in range(1, len(testable) // 2 + 1):

                if len(testable) % chunk_size != 0:
                    continue

                chunks = list(itertools.batched(testable, chunk_size))
                assert all(len(chunk) == chunk_size for chunk in chunks)
                if all(chunk == chunks[0] for chunk in chunks):
                    total += id
                    print(f"Found repeat with chunk size {chunk_size}: {id}")
                    break
    return total


def main() -> None:
    with open("day02_input.txt", "r") as file:
        lines = file.read().splitlines()
        print(part_one(lines))
        print(part_two(lines))


if __name__ == "__main__":
    main()
