from functools import lru_cache
from typing import Dict, List

from CharacterGrid import CharacterGrid
from util import Point2D, tuple2_add, tuple2_mul, tuple2_scalar_mul

max_counter = 0


def parse_lines(lines: List[str]) -> CharacterGrid:
    return CharacterGrid.from_lines(lines)


def calculate_score(map: CharacterGrid) -> int:
    return sum(map.max_y() + 1 - y for (x, y), v in map.map.items() if v == "O")


def shift_all_rocks(map: CharacterGrid, direction: Point2D = (0, -1)) -> None:
    rocks = [k for (k, v) in map.map.items() if v == "O"]

    # descending sort by the direction we're going. we only care that we move the ones
    # toward the edge first, we don't care about the orthogonal ordering
    for rock_loc in sorted(
        rocks, key=lambda loc: tuple2_scalar_mul(tuple2_mul(direction, loc), -1)
    ):
        # if we're in the map and the space is empty, keep going
        cur = rock_loc
        cur = tuple2_add(cur, direction)
        while (
            cur[0] >= 0
            and cur[1] >= 0
            and cur[0] <= map.max_x()
            and cur[1] <= map.max_y()
            and map.map[cur] == "."
        ):
            cur = tuple2_add(cur, direction)

        # go one step back from where we were, since we went out of bounds
        cur = tuple2_add(cur, tuple2_scalar_mul(direction, -1))
        # swap
        map.map[rock_loc] = "."
        map.map[cur] = "O"


def part_one(lines) -> int:
    map = parse_lines(lines)
    map.render()

    shift_all_rocks(map, direction=(0, -1))
    map.render()
    return calculate_score(map)


def part_two(lines) -> int:
    map = parse_lines(lines)
    map.render()
    states: Dict[int, int] = {}
    scores: Dict[int, int] = {}
    iterations = 1000000000

    cycle_length = 0
    offset = 0
    for i in range(iterations):
        for rotation in [(0, -1), (-1, 0), (0, 1), (1, 0)]:
            shift_all_rocks(map, direction=rotation)

        scores[i] = calculate_score(map)

        hashed_value = hash(tuple(sorted(map.map.items())))

        if hashed_value in states:
            if cycle_length == 0:
                offset = states[hashed_value]
                cycle_length = i - offset
            break
        else:
            states[hashed_value] = i

    return scores[offset + ((iterations - 1 - offset) % cycle_length)]


def main() -> None:
    with open("day14_input.txt", "r") as file:
        lines = file.read().splitlines()
        print(part_one(lines))
        print(part_two(lines))


if __name__ == "__main__":
    main()
