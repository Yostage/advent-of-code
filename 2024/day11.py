import functools
import re
from collections import defaultdict, deque
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


stone_history: Dict[Tuple[str, int], int] = {}


# @cache
def count_stones_after_generation(stone: str, generations: int) -> int:
    work = deque([(stone, generations)])

    sum = 0
    work_ctr = 0
    while work:
        work_ctr += 1
        (stone, generations) = work.popleft()
        if work_ctr % 100000 == 0:
            print(
                f"work_ctr: {work_ctr}, len(work): {len(work)}, processing: {stone}, {generations}"
            )

        if generations == 0:
            sum += 1
            stone_history[(stone, generations)] = 1
            continue

        # cache hit
        if (stone, generations) in stone_history:
            sum += stone_history[(stone, generations)]
            continue

        if stone == "0":
            next = ("1", generations - 1)
            if next in stone_history:
                stone_history[(stone, generations)] = stone_history[next]
                sum += stone_history[next]
            else:
                work.appendleft(("1", generations - 1))
        elif len(stone) % 2 == 0:
            l = (str(int(stone[0 : len(stone) // 2])), generations - 1)
            r = (str(int(stone[len(stone) // 2 :])), generations - 1)
            if l in stone_history and r in stone_history:
                children = stone_history[l] + stone_history[r]
                sum += children
                stone_history[(stone, generations)] = children
                continue
            else:
                work.appendleft(l)
                work.appendleft(r)

        else:
            next = (str(int(stone) * 2024), generations - 1)
            if next in stone_history:
                stone_history[(stone, generations)] = stone_history[next]
                sum += stone_history[next]
            else:
                work.appendleft(next)
    return sum


# iterative version
# def count_stones_after_generation(stone: str, generations: int) -> int:
#     if stone == "0":
#         return count_stones_after_generation("1", generations - 1)
#     elif len(stone) % 2 == 0:
#         return count_stones_after_generation(
#             str(int(stone[0 : len(stone) // 2])), generations - 1
#         ) + count_stones_after_generation(
#             str(int(stone[len(stone) // 2 :])), generations - 1
#         )
#     else:
#         return count_stones_after_generation(
#             str(int(stone) * 2024), generations - 1
#         )


def part_two(lines) -> int:
    stones = parse_lines(lines)
    return sum(count_stones_after_generation(stone, 75) for stone in stones)


def main() -> None:
    with open("day11_input.txt", "r") as file:
        lines = file.read().splitlines()
        print(part_one(lines))
        print(part_two(lines))


if __name__ == "__main__":
    main()
