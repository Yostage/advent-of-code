from functools import lru_cache
from typing import Dict, List

from util import Point2D, tuple2_add, tuple2_mul, tuple2_scalar_mul

CharacterGrid2D = Dict[Point2D, str]


max_counter = 0


class CharacterGrid:
    map: CharacterGrid2D

    _max_x: int = -1
    _max_y: int = -1

    def __init__(self, map: CharacterGrid2D):
        self.map = map

    @lru_cache
    def max_x(self) -> int:
        return max(pt[0] for pt in self.map.keys())

    @lru_cache
    def max_y(self) -> int:
        return max(pt[1] for pt in self.map.keys())

    def width(self) -> int:
        return self.max_x() + 1

    def height(self) -> int:
        return self.max_y() + 1

    def render(self) -> None:
        print()
        for y in range(self.height()):
            print("".join([self.map[(x, y)] for x in range(self.width())]))
        print()


def parse_lines(lines: List[str]) -> CharacterGrid:
    return CharacterGrid(
        map={(x, y): c for y, line in enumerate(lines) for x, c in enumerate(line)}
    )


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
