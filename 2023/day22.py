import functools
import re
from dataclasses import dataclass, field
from functools import cache
from itertools import groupby
from typing import Any, Deque, Dict, List, Set, Tuple, TypeVar

from util import Point2D, Point3D, tuple3_add

Cube = Tuple[Point3D, Point3D, str]
Square = Tuple[Point2D, Point2D]


def point3d_from_coords(s: str) -> Point3D:
    t = tuple(int(x) for x in s.split(","))
    assert len(t) == 3
    return t  # type:ignore


def parse_lines(lines: List[str]) -> List[Cube]:
    ret = []
    for line in lines:
        (left_str, right_str) = line.split("~")
        ret.append((point3d_from_coords(left_str), point3d_from_coords(right_str), "."))
    return ret


def intervals_overlap(a: Point2D, b: Point2D) -> bool:
    (first, second) = sorted((a, b))
    return second[0] <= first[1]


def squares_overlap(s1: Square, s2: Square) -> bool:
    for interval in zip(zip(*s1), zip(*s2)):
        if not intervals_overlap(interval[0], interval[1]):
            return False
    return True


def cubes_share_z_projection(a: Cube, b: Cube) -> bool:
    def cube_to_square(c: Cube) -> Square:
        # drop the tag, and then drop the z
        return tuple(x[:-1] for x in c[:-1])  # type:ignore

    # print(f"Testing {a} vs {b}")
    # print(f"Flattening down to {cube_to_square(a)} vs {cube_to_square(b)}")
    return squares_overlap(cube_to_square(a), cube_to_square(b))


# def drop


def idx_to_letter(idx: int) -> str:
    return chr(ord("A") + idx)


def part_one(lines) -> int:
    cubes = parse_lines(lines)

    for idx, cube in enumerate(cubes):
        # print(f"{idx_to_letter(idx)}: {cube}")
        cubes[idx] = (cube[0], cube[1], idx_to_letter(idx))
        # for idx2, cube2 in enumerate(cubes[idx + 1 :]):
        #     print(
        #         f"{idx_to_letter(idx)} vs {idx_to_letter(idx+idx2+1)}: {cubes_share_z_projection(cube,cube2)}"
        #     )

    # first drop all cubes
    # all cubes fall down
    supporting_cubes = set()
    cubes.sort(key=lambda cube: cube[0][2])
    for idx, cube in enumerate(cubes):
        # find its boundary, which is either the top of the cubes under it, or the ground
        below_cubes = [c for c in cubes[:idx] if cubes_share_z_projection(cube, c)]
        below_cubes.sort(key=lambda cube: -cube[1][2])
        # print(f"Cubes below {cube[2]}: {','.join([c[2] for c in below_cubes])}")
        if len(below_cubes) == 0:
            # print(f"Cube {cube[2]} can fall")
            ceiling = 0
        else:
            by_height = {k: v for k, v in groupby(below_cubes, key=lambda c: c[1][2])}
            (sort_key, values) = next(groupby(below_cubes, key=lambda c: -c[1][2]))
            ceiling = -sort_key
            supporter_list = list(values)
            # print(
            #     f"Cube {cube[2]} is supported by {','.join([c[2] for c in supporter_list])}"
            # )
            if len(supporter_list) == 1:
                supporting_cubes.add(supporter_list[0])

        delta = cube[0][2] - (ceiling + 1)
        translation = (0, 0, -delta)
        new_cube = (
            tuple3_add(cube[0], translation),
            tuple3_add(cube[1], translation),
            cube[2],
        )
        # print(f"After translating by {delta},  {new_cube}")
        cubes[idx] = new_cube

    return len(cubes) - len(supporting_cubes)


def part_two(lines) -> int:
    parse_lines(lines)
    return 0


def main() -> None:
    with open("day22_input.txt", "r") as file:
        lines = file.read().splitlines()
        print(part_one(lines))
        print(part_two(lines))


if __name__ == "__main__":
    main()
