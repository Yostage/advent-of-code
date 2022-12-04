import functools
import itertools
from typing import Iterator, List


def input_string_to_intervals(s: str):
    # "2-4,6-8" => (2,4),(6,8)
    pairs = s.split(",")
    assert len(pairs) == 2
    first = [int(i) for i in pairs[0].split("-")]
    assert len(first) == 2
    second = [int(i) for i in pairs[1].split("-")]
    assert len(second) == 2
    return [first, second]


def compare_intervals(a, b) -> int:
    # otherwise sort by first interval ascending
    if a[0] != b[0]:
        return a[0] - b[0]
    else:  # tie break on length, descending
        return (b[1] - b[0]) - (a[1] - a[0])


def intervals_completely_overlap(intervals) -> bool:
    assert len(intervals) == 2
    intervals.sort(key=functools.cmp_to_key(compare_intervals))
    return intervals[0][0] <= intervals[1][0] and intervals[0][1] >= intervals[1][1]


# including when they touch
def intervals_overlap(intervals) -> bool:
    assert len(intervals) == 2
    intervals.sort(key=functools.cmp_to_key(compare_intervals))
    # the second LHS needs to be >= the lft and <= the right
    return intervals[1][0] >= intervals[0][0] and intervals[1][0] <= intervals[0][1]


def main():
    with open("day4_input.txt", "r") as file:
        intervalList = [
            input_string_to_intervals(line) for line in file.read().splitlines()
        ]
        matches = [1 if intervals_overlap(i) else 0 for i in intervalList]
        print(sum(matches))


if __name__ == "__main__":
    main()
