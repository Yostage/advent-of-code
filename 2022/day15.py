import functools
import re
from collections import defaultdict
from dataclasses import dataclass, field
from functools import cache
from typing import Any, Dict, List, Tuple, TypeVar


class Scanner:
    map: defaultdict[Tuple[int, int], str]

    def __init__(self):
        self.map = defaultdict(lambda: ".")

    def test_empty(self, loc: Tuple[int, int]) -> bool:
        return self.map[loc] == "."

    def render(self):
        print()
        min_x = min(k[0] for k, v in self.map.items() if v != ".")
        max_x = max(k[0] for k, v in self.map.items() if v != ".")
        min_y = min(k[1] for k, v in self.map.items() if v != ".")
        max_y = max(k[1] for k, v in self.map.items() if v != ".")
        for y in range(min_y, max_y + 1):
            print("".join([self.map[(x, y)] for x in range(min_x, max_x + 1)]))
        print()


@dataclass
class Sensor:
    loc: Tuple[int, int]
    nearest_beacon: Tuple[int, int]


def parse_lines(lines: List[str]) -> Any:
    sensors: List[Sensor] = []
    for line in lines:
        if match := re.search(
            r"Sensor at x=(.*), y=(.*): closest beacon is at x=(.*), y=(.*)", line
        ):
            (x1, y1, x2, y2) = match.groups()
            sensors.append(
                Sensor(loc=(int(x1), int(y1)), nearest_beacon=(int(x2), int(y2)))
            )
    return sensors


def part_one(lines) -> int:
    sensors = parse_lines(lines)
    s = Scanner()
    for sensor in sensors:
        s.map[sensor.loc] = "S"
        s.map[sensor.nearest_beacon] = "B"

    s.render()
    return 0


def part_two(lines) -> int:
    parse_lines(lines)
    return 0


def main() -> None:
    with open("day15_input.txt", "r") as file:
        lines = file.read().splitlines()
        print(part_one(lines))
        print(part_two(lines))


if __name__ == "__main__":
    main()
