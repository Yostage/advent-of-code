import re
from collections import defaultdict
from dataclasses import dataclass
from typing import List, Optional, Tuple

Point2D = Tuple[int, int]


def manhattan_distance(a: Point2D, b: Point2D) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


@dataclass
class Sensor:
    loc: Point2D
    nearest_beacon: Point2D

    def blackout_distance(self) -> int:
        return manhattan_distance(self.loc, self.nearest_beacon)

    def coverage_interval_at_row(self, row: int) -> Point2D:
        dx = self.blackout_distance() - abs(self.loc[1] - row)
        if dx < 0:
            return (-1, -1)
        return (self.loc[0] - dx, self.loc[0] + dx)


class Scanner:
    map: defaultdict[Point2D, str]
    sensors: List[Sensor]

    def __init__(self):
        self.map = defaultdict(lambda: ".")

    def test_empty(self, loc: Point2D) -> bool:
        return self.map[loc] == "."

    def test_possible_beacon(self, loc: Point2D) -> bool:
        assert self.sensors is not None
        # print(f"Testing {loc}")
        return all(
            loc == s.nearest_beacon
            or manhattan_distance(loc, s.loc) > s.blackout_distance()
            for s in self.sensors
        )

    def blackout_squares(self, center: Point2D, radius: int):
        for x in range(center[0] - radius, center[0] + radius + 1):
            dy = radius - abs(center[0] - x)
            for y in range(center[1] - dy, center[1] + dy + 1):
                if self.test_empty((x, y)):
                    self.map[(x, y)] = "#"

    def render(self):
        print()
        min_x = min(k[0] for k, v in self.map.items() if v != ".")
        max_x = max(k[0] for k, v in self.map.items() if v != ".")
        min_y = min(k[1] for k, v in self.map.items() if v != ".")
        max_y = max(k[1] for k, v in self.map.items() if v != ".")
        for y in range(min_y, max_y + 1):
            print("".join([self.map[(x, y)] for x in range(min_x, max_x + 1)]))
        print()


def parse_lines(lines: List[str]) -> List[Sensor]:
    sensors: List[Sensor] = []
    for line in lines:
        if match := re.search(
            r"Sensor at x=(.*), y=(.*): closest beacon is at x=(.*), y=(.*)", line
        ):
            (x1, y1, x2, y2) = match.groups()
            sensors.append(
                Sensor(loc=(int(x1), int(y1)), nearest_beacon=(int(x2), int(y2)))
            )
        else:
            assert False
    return sensors


def part_one(lines, row) -> int:
    sensors = parse_lines(lines)
    m = Scanner()
    m.sensors = sensors
    for sensor in sensors:
        m.map[sensor.loc] = "S"
        m.map[sensor.nearest_beacon] = "B"
        # m.blackout_squares(sensor.loc, sensor.blackout_distance())
        print(f"Sensor distance = {sensor.blackout_distance()}")

    min_x = min(s.loc[0] - s.blackout_distance() for s in sensors)
    max_x = max(s.loc[0] + s.blackout_distance() for s in sensors)

    # m.render()
    return sum([not m.test_possible_beacon((x, row)) for x in range(min_x, max_x + 1)])


def intervals_touch(l: Point2D, r: Point2D) -> bool:
    return r[0] <= l[1] + 1


def find_gap(intervals: List[Point2D], max_edge: int) -> Optional[int]:
    # print(f"intervals = {intervals}")
    lhs = intervals.pop(0)
    for rhs in intervals:
        # each interval must overlap. if they don't, we've found the gap
        # and we're only allowed one gap
        if intervals_touch(lhs, rhs):
            # smoosh em
            lhs = (min(lhs[0], rhs[0]), max(lhs[1], rhs[1]))
            continue
        # otherwise we must have a single pace gap after the lhs
        print(f"Found failure to overlap at {lhs} vs {rhs}")
        assert lhs[1] + 1 == rhs[0] - 1
        return lhs[1] + 1

    # we got a maxi-interval, but does it touch the edges?
    if lhs[0] <= 0 and lhs[1] >= max_edge:
        return None
    elif lhs[0] == 1:
        return 0
    elif lhs[1] == max_edge - 1:
        return max_edge
    else:
        raise AssertionError(f"Gap too big {lhs}")


def part_two(lines: List[str], max_edge: int) -> int:
    parse_lines(lines)
    sensors = parse_lines(lines)
    m = Scanner()
    m.sensors = sensors
    for sensor in sensors:
        m.map[sensor.loc] = "S"
        m.map[sensor.nearest_beacon] = "B"
        # m.blackout_squares(sensor.loc, sensor.blackout_distance())
        # print(f"Sensor distance = {sensor.blackout_distance()}")

    beacons = set([s.nearest_beacon for s in sensors])
    # this way is extremely bad
    # for y in range(0, max_edge + 1):
    #     for x in range(0, max_edge + 1):
    #         if x == 0:
    #             print(f"Testing row {y} out of {max_edge}")
    #         if m.test_possible_beacon((x, y)) and (x, y) not in beacons:
    #             print(f"Chose beacon loc {(x,y)}")
    #             return x * 4000000 + y
    for y in range(0, max_edge + 1):
        if y % 1000 == 0:
            print(f"Testing row {y}")
        intervals = list(
            sorted(
                filter(
                    lambda x: x != (-1, -1),
                    [s.coverage_interval_at_row(y) for s in sensors],
                )
            )
        )

        # merge them all together
        if result := find_gap(intervals, max_edge):
            print(f"Chose beacon loc {result}")
            return result * 4000000 + y

    raise AssertionError("No space found")


def main() -> None:
    with open("day15_input.txt", "r") as file:
        lines = file.read().splitlines()
        # print(part_one(lines, 2000000))
        print(part_two(lines, 4000000))


if __name__ == "__main__":
    main()
