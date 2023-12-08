import functools
import re
from dataclasses import dataclass, field
from functools import cache
from typing import Any, Dict, List, TypeVar


@dataclass
class RangeMapping:
    dest_start: int
    source_start: int
    range: int

    def matches_seed(self, seed) -> bool:
        return seed >= self.source_start and seed < self.source_start + self.range

    def translate_seed(self, seed: int) -> int:
        assert self.matches_seed(seed)
        return self.dest_start + (seed - self.source_start)


@dataclass
class Almanac:
    seeds: List[int]
    maps: List[List[RangeMapping]]

    def translate_seed(self, seed: int):
        # print(f"Translating seed {seed}")
        for idx, map in enumerate(self.maps):
            for mapping in map:
                if mapping.matches_seed(seed):
                    seed = mapping.translate_seed(seed)
                    break
            # print(f"Map {idx}: seed = {seed}")
        return seed


def parse_lines(lines: List[str]) -> Any:
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

            # todo close map

        numbers = [int(n) for n in line.split(" ")]
        assert len(numbers) == 3
        ranges.append(
            RangeMapping(
                dest_start=numbers[0], source_start=numbers[1], range=numbers[2]
            )
        )

    maps.append(ranges)
    return Almanac(seeds=seeds, maps=maps)


def part_one(lines) -> int:
    almanac = parse_lines(lines)
    locations = [almanac.translate_seed(seed) for seed in almanac.seeds]
    return min(locations)


def part_two(lines) -> int:
    parse_lines(lines)
    return 0


def main() -> None:
    with open("day05_input.txt", "r") as file:
        lines = file.read().splitlines()
        print(part_one(lines))
        print(part_two(lines))


if __name__ == "__main__":
    main()
