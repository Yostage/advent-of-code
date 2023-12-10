import functools
import re
from dataclasses import dataclass, field
from functools import cache
from itertools import islice
from typing import Any, Dict, List, Tuple, TypeVar

from more_itertools import batched

from util import Point2D, tuple2_add

# first: |-----|
# second:         |----------|
# first:                  |-----|
# second:   |----------|

# first:      |-----|
# second:   |----------|
# first:  |---------------|
# second:   |----------|

# first:           |-----|
# second:   |----------|

# first: |-----|
# second:   |----------|


# left:  |-|
# middle    |--|
# right:        |------|
def split_interval(first: Point2D, second: Point2D):
    if first[0] < second[0]:
        left = (first[0], min(first[1], second[0] - 1))
    else:
        left = None

    if first[1] > second[1]:
        right = (max(second[1] + 1, first[0]), first[1])
    else:
        right = None

    if first[1] < second[0] or first[0] > second[1]:
        middle = None
    else:
        middle = (max(first[0], second[0]), min(second[1], first[1]))

    return (left, middle, right)


@dataclass
class RangeMapping:
    dest_start: int
    source_start: int
    range: int

    def matches_seed(self, seed: int) -> bool:
        return seed >= self.source_start and seed < self.source_start + self.range

    # def matches_seed_range(self, seed_range: Point2D) -> bool:
    # source_tuple = (self.source_start, self.source_start + self.range)
    # intervals = sorted([source_tuple, seed_range])

    # return intervals[0][1] >= intervals[1][0]

    # def translate_seed_range(self, seed_range: Point2D) -> bool:
    # assert self.matches_seed_range(seed_range)
    # turn into left/middle/right
    # if middle, translate middle, add middle to done bucket
    # flatten left and right and put them into next bucket

    def translate_seed(self, seed: int) -> int:
        assert self.matches_seed(seed)
        return self.dest_start + (seed - self.source_start)


@dataclass
class Almanac:
    seeds: List[int]
    maps: List[List[RangeMapping]]

    def translate_seed_day_one(self, seed: int):
        # print(f"Translating seed {seed}")
        for idx, map in enumerate(self.maps):
            for mapping in map:
                if mapping.matches_seed(seed):
                    seed = mapping.translate_seed(seed)
                    break
            # print(f"Map {idx}: seed = {seed}")
        return seed


def parse_lines(lines: List[str]) -> Almanac:
    # first line: seeds
    seeds = [int(s) for s in lines[0][len("seeds: ") :].split(" ")]
    # maps after this
    ranges: List[RangeMapping] = []
    maps: List[List[RangeMapping]] = []
    for line in lines[1:]:
        # seeds

        # blank lines
        if len(line) == 0:
            continue

        if "map" in line:
            if len(ranges) > 0:
                maps.append(ranges)
                ranges = []
            continue

        numbers = [int(n) for n in line.split(" ")]
        assert len(numbers) == 3
        ranges.append(
            RangeMapping(
                dest_start=numbers[0], source_start=numbers[1], range=numbers[2]
            )
        )

    # close terminal map
    maps.append(ranges)
    return Almanac(seeds=seeds, maps=maps)


def part_one(lines) -> int:
    almanac = parse_lines(lines)
    locations = [almanac.translate_seed_day_one(seed) for seed in almanac.seeds]
    return min(locations)


def part_two(lines) -> int:
    def process_mapping(
        mapping: RangeMapping, seeds: List[Point2D]
    ) -> Tuple[List[Point2D], List[Point2D]]:
        mapping_interval = (
            mapping.source_start,
            mapping.source_start + mapping.range,
        )
        output = []
        finished = []
        for seed in seeds:
            (l, m, r) = split_interval(seed, mapping_interval)
            # print(f"\t\t {seed} against {mapping_interval} -> [{l}, {m}, {r}]")
            if m:
                m = tuple2_add(
                    m,
                    (
                        mapping.dest_start - mapping.source_start,
                        mapping.dest_start - mapping.source_start,
                    ),
                )
                # print(f"\t\t Translated to {m}")
                # don't let this range get touched again
                finished.append(m)
            if l:
                output.append(l)
            if r:
                output.append(r)
        return (output, finished)

    def process_map(map: List[RangeMapping], seeds: List[Point2D]) -> List[Point2D]:
        unmatched = seeds
        finished: List[Point2D] = []
        for mapping in map:
            (unmatched, matched) = process_mapping(mapping, unmatched)
            finished.extend(matched)
        finished.extend(unmatched)
        return finished

    def process_seed(almanac: Almanac, seed: Point2D) -> List[Point2D]:
        # print(f"Parsing seed range {seed}")
        seeds = [seed]
        for map in almanac.maps:
            # print(f"\tNew map")
            seeds = process_map(map, seeds)
        return seeds

    almanac = parse_lines(lines)
    seed_ranges = [
        (chunk[0], chunk[0] + chunk[1] - 1) for chunk in batched(almanac.seeds, 2)
    ]

    output_ranges: List[Point2D] = []
    for seed in seed_ranges:
        output_ranges.extend(process_seed(almanac, seed))

    return min([r[0] for r in output_ranges])


def main() -> None:
    with open("day05_input.txt", "r") as file:
        lines = file.read().splitlines()
        print(part_one(lines))
        print(part_two(lines))


if __name__ == "__main__":
    main()
