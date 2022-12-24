from collections import deque
from typing import Deque, FrozenSet, List, Set, Tuple

from CallCounter import CallCounter

Point3D = Tuple[int, int, int]

CubeSet = FrozenSet[Point3D]


def tuple3_add(a: Point3D, b: Point3D) -> Point3D:
    return tuple(map(sum, zip(a, b)))  # type: ignore


all_3d_vectors = (
    (1, 0, 0),
    (-1, 0, 0),
    (0, 1, 0),
    (0, -1, 0),
    (0, 0, 1),
    (0, 0, -1),
)


def parse_lines(lines: List[str]) -> CubeSet:
    cubes: Set[Point3D] = set()
    for line in lines:
        strings = line.split(",")
        cubes.add(tuple(map(int, strings)))  # type: ignore

    return frozenset(cubes)


def part_one(lines: List[str]) -> int:
    cubes = parse_lines(lines)
    open_sides = 0
    for cube in cubes:
        for side in all_3d_vectors:
            test = tuple3_add(cube, side)
            if not test in cubes:
                # print(f"Open side {test}")
                open_sides += 1
    return open_sides


def get_bounding_box(cubes: CubeSet) -> Tuple[Point3D, Point3D]:
    mins = [min([c[x] for c in cubes]) for x in [0, 1, 2]]
    maxes = [max([c[x] for c in cubes]) for x in [0, 1, 2]]
    return (tuple(mins), tuple(maxes))  # type: ignore


def find_all_exposed(
    cubes: CubeSet, bounding_box: Tuple[Point3D, Point3D]
) -> FrozenSet[Point3D]:
    queue: Deque[Point3D] = deque()

    # stretch the bounding box so we can walk around it
    min_corner = tuple3_add(bounding_box[0], (-1, -1, -1))
    max_corner = tuple3_add(bounding_box[1], (1, 1, 1))

    def inside_bounding_box(p: Point3D):
        return all(pair[0] >= pair[1] for pair in zip(p, min_corner)) and all(
            pair[0] <= pair[1] for pair in zip(p, max_corner)
        )

    queue.append(min_corner)
    exposed = set()

    while len(queue) > 0:
        visiting = queue.pop()
        exposed.add(visiting)

        # add every edge if it's in the new bounding box and not a cube
        for neighbor in [tuple3_add(visiting, vec) for vec in all_3d_vectors]:
            if (
                inside_bounding_box(neighbor)
                and not neighbor in cubes
                and not neighbor in exposed
                and not neighbor in queue
            ):
                queue.append(neighbor)

    print(f"Found {len(exposed)} exposed squares")
    return frozenset(exposed)


def part_two(lines: List[str]) -> int:
    CallCounter.clear()
    cubes = parse_lines(lines)
    open_sides = 0
    bounding_box = get_bounding_box(cubes)
    print(f"Bounding box at {bounding_box}")

    all_exposed = find_all_exposed(cubes, bounding_box)
    for cube in cubes:
        for vec in all_3d_vectors:
            candidate = tuple3_add(vec, cube)
            if candidate in all_exposed:
                open_sides += 1
    print(CallCounter.counts())
    return open_sides


def main() -> None:
    with open("day18_input.txt", "r") as file:
        lines = file.read().splitlines()
        print(part_one(lines))
        print(part_two(lines))


if __name__ == "__main__":
    main()
