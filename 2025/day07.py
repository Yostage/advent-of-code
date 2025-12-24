from functools import lru_cache

from CharacterGrid import CharacterGrid
from util import Point2D


def parse_lines(lines: list[str]) -> CharacterGrid:
    return CharacterGrid.from_lines(lines)


def part_one(lines) -> int:
    def split_laser(grid: CharacterGrid, pt: Point2D) -> None:
        left = (pt[0] - 1, pt[1] + 1)
        right = (pt[0] + 1, pt[1] + 1)
        for pt in [left, right]:
            if grid.map.get(pt) == ".":
                grid.map[pt] = "|"

    grid = parse_lines(lines)
    total = 0
    for y in range(grid.height()):
        for x in range(grid.width()):
            p = (x, y)
            if grid.map.get(p) == "S":
                grid.map[(p[0], p[1] + 1)] = "|"
            if grid.map.get(p) == "|":
                dest = (p[0], p[1] + 1)
                if grid.map.get(dest) == ".":
                    grid.map[dest] = "|"
                elif grid.map.get(dest) == "^":
                    total += 1
                    split_laser(grid, dest)

    grid.render()
    return total


@lru_cache
def recursive_splitter(grid: CharacterGrid, pt: Point2D) -> int:
    def walk_down(grid: CharacterGrid, pt: Point2D) -> int:
        while True:
            if grid.map.get(pt) is None:
                return 0
            if grid.map.get(pt) == "^":
                return recursive_splitter(grid, pt)
            pt = (pt[0], pt[1] + 1)

    left = (pt[0] - 1, pt[1] + 1)
    right = (pt[0] + 1, pt[1] + 1)
    return 1 + walk_down(grid, left) + walk_down(grid, right)


def part_two(lines) -> int:
    total = 0
    grid = parse_lines(lines)
    for y in range(grid.height()):
        row = grid.get_row_string(y)
        x = row.find("S")
        if x != -1:
            break  # found the start point
    # print(f"Start point is at ({x}, {y})")
    while grid.map.get((x, y)) != "^":
        y += 1
    # print(f"First splitter is at ({x}, {y})")
    return 1 + recursive_splitter(grid, (x, y))
    # find the first splitter in the world

    return total


def main() -> None:
    with open("day07_input.txt", "r") as file:
        lines = file.read().splitlines()
        print(part_one(lines))
        print(part_two(lines))


if __name__ == "__main__":
    main()
    main()
