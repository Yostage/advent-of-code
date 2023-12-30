from itertools import count
from typing import Dict, List

from util import Point2D

MirrorMap = Dict[Point2D, str]


def parse_lines(lines: List[str]) -> List[MirrorMap]:
    def lines_to_map(lines: List[str]):
        return {(x, y): c for y, line in enumerate(lines) for x, c in enumerate(line)}

    maps: List[MirrorMap] = []
    current_lines: List[str] = []
    # inject terminator so we don't have to handle that case
    lines = lines.copy()
    lines.append("")
    for line in lines:
        if len(line) == 0:
            maps.append(lines_to_map(current_lines))
            current_lines = []
        else:
            current_lines.append(line)

    return maps


def test_column(map: MirrorMap, pivot_column: int) -> bool:
    max_x = max(pt[0] for pt in map.keys())
    max_y = max(pt[1] for pt in map.keys())
    for offset in count(0):
        lhs = pivot_column - offset
        rhs = pivot_column + 1 + offset

        # we've compared them all
        if lhs < 0:
            return True
        if rhs > max_x:
            return True
        l_vec = tuple(map[(lhs, y)] for y in range(0, max_y + 1))
        r_vec = tuple(map[(rhs, y)] for y in range(0, max_y + 1))
        if l_vec != r_vec:
            return False
    return True


def test_row(map: MirrorMap, pivot_row: int) -> bool:
    max_x = max(pt[0] for pt in map.keys())
    max_y = max(pt[1] for pt in map.keys())
    for offset in count(0):
        top = pivot_row - offset
        bottom = pivot_row + 1 + offset

        # we've compared them all
        if top < 0:
            return True
        if bottom > max_y:
            return True
        t_vec = tuple(map[(x, top)] for x in range(0, max_x + 1))
        b_vec = tuple(map[(x, bottom)] for x in range(0, max_x + 1))
        if t_vec != b_vec:
            return False
    return True


def parse_map(map: MirrorMap) -> List[int]:
    # check every horizontal gap
    results: List[int] = []
    max_y = max(pt[1] for pt in map.keys())
    max_x = max(pt[0] for pt in map.keys())
    for pivot_column in range(0, max_x):
        if test_column(map, pivot_column):
            results.append(pivot_column + 1)

    for pivot_row in range(0, max_y):
        if test_row(map, pivot_row):
            results.append(100 * (pivot_row + 1))
    return results


def deep_parse_map(map: MirrorMap) -> int:
    def opposite(s: str) -> str:
        if s == ".":
            return "#"
        if s == "#":
            return "."
        assert False

    base_case = parse_map(map)
    for k, v in map.items():
        clone = map.copy()
        clone[k] = opposite(v)
        new_result = parse_map(clone)
        filtered = [x for x in new_result if x not in base_case]
        if len(filtered) > 0:
            return filtered[0]

    assert False

    return 0


def part_one(lines) -> int:
    maps = parse_lines(lines)
    return sum(parse_map(map)[0] for map in maps)


def part_two(lines) -> int:
    maps = parse_lines(lines)
    return sum(deep_parse_map(map) for map in maps)


def main() -> None:
    with open("day13_input.txt", "r") as file:
        lines = file.read().splitlines()
        print(part_one(lines))
        print(part_two(lines))


if __name__ == "__main__":
    main()
