import functools
import re
from collections import defaultdict
from dataclasses import dataclass, field
from functools import cache
from multiprocessing import Value
from typing import Any, Deque, Dict, List, Set, Tuple, TypeVar

from PIL import Image

from CharacterGrid import CharacterGrid, orthogonal_adjacencies
from util import Point2D, tuple2_add


def parse_lines(lines: List[str]) -> Any:
    return CharacterGrid.from_lines(lines)


def part_one(lines) -> int:
    grid = parse_lines(lines)

    if grid.max_x() == 10:
        steps = 6
    elif grid.max_x() == 130:
        steps = 64
    else:
        raise ValueError(grid.max_x())

    next_gen: Set[Point2D] = set(k for k, v in grid.map.items() if v == "S")
    assert len(next_gen) == 1
    for generation in range(steps):
        last_gen = next_gen
        next_gen = set()
        for space in last_gen:
            for adj in orthogonal_adjacencies:
                candidate = tuple2_add(space, adj)
                if grid.map.get(candidate) in ["S", "."]:
                    next_gen.add(candidate)
        # print(
        #     f"generation:{generation}: from {len(last_gen)} plots to {len(next_gen)} plots"
        # )

    return len(next_gen)


def save_image(generation: int, visited: Set[Point2D]) -> None:
    # PIL accesses images in Cartesian co-ordinates, so it is Image[columns, rows]
    min_x = min(pt[0] for pt in visited)
    max_x = max(pt[0] for pt in visited)
    min_y = min(pt[1] for pt in visited)
    max_y = max(pt[1] for pt in visited)

    print(f"Creating image {max_x - min_x} by {max_y-min_y}")
    img = Image.new(
        "RGB", (1 + max_x - min_x, 1 + max_y - min_y), "black"
    )  # create a new black image
    pixels = img.load()  # create the pixel map
    # for (x,y), c in grid.map.items():
    for x, y in visited:
        # for i in range(img.size[0]):  # for every col:
        # for j in range(img.size[1]):  # For every row
        pixels[x - min_x, y - min_y] = (255, 255, 255)

    img.save(f"day21_generation_{generation:04}.png")


def part_two(lines, steps) -> int:
    grid = parse_lines(lines)

    # if grid.width() == 11:
    #     steps = 6
    # elif grid.width() == 131:
    #     # steps = 250
    #     steps = 327
    # else:
    #     raise ValueError(grid.max_x())

    next_gen: Set[Point2D] = set(k for k, v in grid.map.items() if v == "S")
    assert len(next_gen) == 1
    scores = {}
    a = {}
    b = {}
    cd = {}
    # for generation in range(1, steps + 1):
    # for generation in range(1, 470):
    #     last_gen = next_gen
    #     next_gen = set()
    #     for space in last_gen:
    #         for adj in orthogonal_adjacencies:
    #             candidate = tuple2_add(space, adj)
    #             translated_candidate = (
    #                 candidate[0] % grid.width(),
    #                 candidate[1] % grid.height(),
    #             )
    #             if grid.map[translated_candidate] in ["S", "."]:
    #                 next_gen.add(candidate)
    #     score = len(next_gen)
    #     scores[generation] = score
    #     # if generation % 10 == 0:
    #     #     save_image(generation, next_gen)

    #     # if generation % 131 == 65 or generation == 64:
    #     radius = (generation // grid.width()) + 1
    #     offset = generation % grid.width()
    #     parity = generation % 2
    #     if offset in (grid.width() // 2, (grid.width() // 2) - 1):
    #         if radius == 1:
    #             a[parity] = score

    #         # save_image(generation, next_gen)
    #         print(
    #             f"Gen {generation} | mod {generation % grid.width()} : marks = {scores[generation]}"
    #         )
    scores = {
        64: 3637,
        65: 3699,
        195: 32947,
        196: 33137,
        326: 91633,
        327: 91951,
        457: 179695,
        458: 180141,
        # 330: -1,
        steps: -1,
    }
    #     Gen 64 | mod 64 : marks = 3637
    # Gen 65 | mod 65 : marks = 3699
    # Gen 195 | mod 64 : marks = 32947
    # Gen 196 | mod 65 : marks = 33137
    # Gen 326 | mod 64 : marks = 91633
    # Gen 327 | mod 65 : marks = 91951

    # retcon
    score_by_gen: defaultdict[int, Dict[int, int]] = defaultdict(dict)
    for offset in [0, -1]:
        for generation in [0, 1, 2]:
            step_count = offset + (generation * grid.width()) + (grid.width() // 2)
            print(f"Saving score for step {step_count}")
            score_by_gen[generation][step_count % 2] = scores[step_count]

    # for parity in [0, 1]:
    #     a[parity] = score_by_gen[0][parity]
    #     cd[parity] = (
    #         score_by_gen[2][parity] - score_by_gen[1][parity] - (8 * a[parity])
    #     ) / 4
    # b[parity] = (score_by_gen[1][parity] - a[parity] - (2 * cd[parity])) / 4

    # a = {0: score_by_gen[0][0]}

    a = {1: scores[65], 0: scores[64]}
    b = {0: a[1], 1: a[0]}
    cd = {k: (scores[196] - a[0] - (4 * b[0])) / 2 for k in [0, 1]}
    # b[0] = a[1]
    print(f"A={a} | B={b} | CD = {cd}")

    # for gen in [0, 1, 2]:
    #     for offset in [-1, 0]:
    for step in sorted(scores.keys()):
        gen = step // grid.width()
        # step = gen * grid.width() + grid.width() // 2 + offset
        parity = step % 2
        a_coefficient = pow(1 + (2 * (gen // 2)), 2)
        b_coefficient = pow(2 * ((gen + 1) // 2), 2)
        cd_coefficient = gen * (gen + 1)
        print(f"Checking step {step}")
        print(
            f"\ta_c  = {a_coefficient} | b_c = {b_coefficient} | cd_c = {cd_coefficient}"
        )
        score_calc = (
            a[parity] * a_coefficient
            + b[parity] * b_coefficient
            + cd[parity] * cd_coefficient
        )
        print(f"\tReal score {scores.get(step, '??')} vs calculated score {score_calc}")

    return scores[steps]


def main() -> None:
    with open("day21_input.txt", "r") as file:
        lines = file.read().splitlines()
        print(part_one(lines))
        print(part_two(lines, steps=26501365))
        # print(part_two(lines, steps=330))
        # 26501365


if __name__ == "__main__":
    main()
