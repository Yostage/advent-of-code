import functools
import re
from dataclasses import dataclass, field
from functools import cache
from typing import Any, Dict, Iterable, List, Tuple, TypeVar


def parse_lines(lines: List[str]) -> List[Tuple[str, List[int]]]:
    ret = []
    for line in lines:
        (springs, seg_string) = line.split(" ")
        segments = [int(s) for s in seg_string.split(",")]
        ret.append((springs, segments))
    return ret


def how_many_legal(springs: str, segments: List[int]) -> int:
    # base case
    if len(segments) == 0:
        if "#" in springs:
            # print(f"illegal terminal state: {springs}")
            return 0
        else:
            # print(f"base case: {springs}")
            return 1

    # otherwise
    pattern = rf"^(\?|#){{{segments[0]}}}(\.|\?|$)"
    # print(pattern)

    sum = 0
    for i in range(0, len(springs)):
        if match := re.match(pattern, springs[i:]):
            # print(
            #     f"Matched: {segments[0]} against str {springs[i:]}, length {len(match.group())}"
            # )
            sum += how_many_legal(springs[i + len(match.group()) :], segments[1:])
        # else:
        #     print(f"No match: {segments[0]} [{pattern}] against str {springs[i:]}")
        # if we had a spring here, but we didn't match it, we cannot recurse further
        if springs[i:][0] == "#":
            # print("Cannot recurse further, spring starts with a #")
            return sum
    return sum


# def how_many_legal(runs, segments) -> int:
#     # base case: we've placed all the segments
#     if len(segments) == 0:
#         # this is legal
#         return 1
#     # we always want to try to consume the first segment

#     sum = 0
#     runs = runs.copy()

#     while len(runs) > 0:
#         # completely skip runs of fixed springs, we can't use them
#         if runs[0][0] == ".":
#             runs.pop(0)
#             continue

#         # this is a broken run. We have to use it, or else this state is illegal
#         if runs[0][0] == "#":
#             # illegal state, we cannot place the next segment
#             if runs[0][1] != segments[0]:
#                 return 0
#             # legal state, we must use the next segment, and we do not fork
#             return how_many_legal(runs[1:], segments[1:])

#         assert runs[0][0] == "?"

#         # the case where we don't use it at all, which consumes no segments
#         sum += how_many_legal(runs[1:], segments)
#         for skip in range(segments[0], runs[0][1]):
#             remaining_run
#             sum += how_many_legal(, segments[1:])

#     return sum
#     # now

#     # for each remaining unknown spring_interval
#     # there are zero or more ways to consume it
#     # don't forget to calculate if we need to terminate it as well
#     # find all the places that we can put this first segment, including adding a
#     # terminator after it

#     # then we memoize
#     # then we multiprocess
#     return 7


# def springs_to_runs(springs: str) -> List[Tuple[str, int]]:
#     ret: List[Tuple[str, int]] = []
#     run_length = 0
#     current_char = "X"
#     for c in springs:
#         if c != current_char:
#             # new interval
#             # skip first interval ever
#             if current_char != "X":
#                 ret.append((current_char, run_length))
#             current_char = c
#             run_length = 1
#         else:
#             run_length += 1
#     # close the dangling interval
#     ret.append((current_char, run_length))

#     return ret


def part_one(lines) -> int:
    data = parse_lines(lines)
    sum = 0
    for springs, segments in data:
        # runs = springs_to_runs(springs)
        # answer = how_many_legal(runs, segments)
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
