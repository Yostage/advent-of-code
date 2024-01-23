import functools
import re
from collections import defaultdict
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


def day_22_internal(lines) -> Tuple[int, int]:
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
    # supporting_cubes = set()

    cube_to_below_cubes: Dict[str, Set[str]] = {}
    # supported_by = defaultdict(set)
    cube_to_above_cubes = defaultdict(set)
    cubes.sort(key=lambda cube: cube[0][2])
    for idx, cube in enumerate(cubes):
        # find its boundary, which is either the top of the cubes under it, or the ground
        below_cubes = [c for c in cubes[:idx] if cubes_share_z_projection(cube, c)]
        below_cubes.sort(key=lambda cube: -cube[1][2])
        # print(f"Cubes below {cube[2]}: {','.join([c[2] for c in below_cubes])}")
        if len(below_cubes) == 0:
            # print(f"Cube {cube[2]} can fall")
            ceiling = 0
            cube_to_below_cubes[cube[2]] = set()
        else:
            by_height = {k: v for k, v in groupby(below_cubes, key=lambda c: c[1][2])}
            (sort_key, values) = next(groupby(below_cubes, key=lambda c: -c[1][2]))
            ceiling = -sort_key
            supported_by_keys = list(v[2] for v in values)
            for value in supported_by_keys:
                cube_to_above_cubes[value].add(cube[2])

            cube_to_below_cubes[cube[2]] = set(supported_by_keys)
            # supporter_list = list(values)
            # print(
            #     f"Cube {cube[2]} is supported by {','.join([c[2] for c in supporter_list])}"
            # )
            # if len(supporter_list) == 1:
            # supporting_cubes.add(supporter_list[0])

        delta = cube[0][2] - (ceiling + 1)
        translation = (0, 0, -delta)
        new_cube = (
            tuple3_add(cube[0], translation),
            tuple3_add(cube[1], translation),
            cube[2],
        )
        # print(f"After translating by {delta},  {new_cube}")
        cubes[idx] = new_cube

    # print(support_list)
    # print(supported_by)
    # print(set(list(x)[0] for x in supported_by.values() if len(x) == 1))
    destructible_cubes = len(cubes) - len(
        set(list(x)[0] for x in cube_to_below_cubes.values() if len(x) == 1)
    )

    def count_total_chain_reaction(key: str) -> int:
        next_splode = [key]
        destroyed = set()
        while True:
            if len(next_splode) == 0:
                break
            this_splode = next_splode
            next_splode = []
            # mark all blocks in this wave destroyed
            destroyed.update(this_splode)
            # and mark the next outgoing wave
            for cube in this_splode:
                for block_up in cube_to_above_cubes[cube]:
                    if all(
                        support in destroyed
                        for support in cube_to_below_cubes[block_up]
                    ):
                        next_splode.append(block_up)

        # print(f"Cube {key} chain reaction = {len(destroyed)-1}")
        # we're not allowed to count the initial block in the reaction
        return len(destroyed) - 1

    return (
        destructible_cubes,
        sum(
            count_total_chain_reaction(cube_key)
            for cube_key in cube_to_below_cubes.keys()
        ),
    )


def part_one(lines) -> int:
    return day_22_internal(lines)[0]


def part_two(lines) -> int:
    return day_22_internal(lines)[1]


def main() -> None:
    with open("day22_input.txt", "r") as file:
        lines = file.read().splitlines()
        (one, two) = day_22_internal(lines)
        print(one)
        print(two)


if __name__ == "__main__":
    main()
