import re
from functools import cache
from itertools import chain, repeat
from typing import List, Tuple

from util import CallCounter


def parse_lines(lines: List[str]) -> List[Tuple[str, List[int]]]:
    ret = []
    for line in lines:
        (springs, seg_string) = line.split(" ")
        segments = [int(s) for s in seg_string.split(",")]
        ret.append((springs, segments))
    return ret


@cache
@CallCounter
def how_many_legal(springs: str, segments: Tuple[int]) -> int:
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


def part_one(lines) -> int:
    data = parse_lines(lines)
    sum = 0
    for springs, segments in data:
        answer = how_many_legal(springs, tuple(segments))
        print(f"{springs} : {','.join([str(s) for s in segments])} : {answer}")
        sum += answer

    return sum


def part_two(lines) -> int:
    data = parse_lines(lines)
    sum = 0
    for springs, segments in data:
        springs = "?".join(repeat(springs, 5))
        segments = list(chain.from_iterable(repeat(segments, 5)))
        answer = how_many_legal(springs, tuple(segments))
        print(f"{springs} : {','.join([str(s) for s in segments])} : {answer}")
        sum += answer

    return sum


def main() -> None:
    with open("day12_input.txt", "r") as file:
        lines = file.read().splitlines()
        print(part_one(lines))
        print(CallCounter.counts())
        CallCounter.clear()
        print(part_two(lines))
        print(CallCounter.counts())


if __name__ == "__main__":
    main()
