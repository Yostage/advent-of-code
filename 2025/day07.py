from CharacterGrid import CharacterGrid
from util import Point2D


def parse_lines(lines: list[str]) -> CharacterGrid:
    return CharacterGrid.from_lines(lines)


def part_one(lines) -> int:
    def split_laser(grid: CharacterGrid, pt: Point2D) -> None:
        # left = Point2D(pt.x - 1, pt.y + 1)
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
                # print(f"S at ({x}, {y})")
                grid.map[(p[0], p[1] + 1)] = "|"
            if grid.map.get(p) == "|":
                dest = (p[0], p[1] + 1)
                if grid.map.get(dest) == ".":
                    grid.map[dest] = "|"
                elif grid.map.get(dest) == "^":
                    total += 1
                    split_laser(grid, dest)

                # print(f"S at ({x}, {y})")
                # grid.map[(p[0], p[1] + 1)] = "|"

            # if grid.map.get(p) == "^":

    grid.render()
    return total


def part_two(lines) -> int:
    # grid = parse_lines(lines)
    total = 0
    return total


def main() -> None:
    with open("day07_input.txt", "r") as file:
        lines = file.read().splitlines()
        print(part_one(lines))
        print(part_two(lines))


if __name__ == "__main__":
    main()
