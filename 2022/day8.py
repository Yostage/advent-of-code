from functools import cache
import functools
import re
from typing import Any, Dict, List


from dataclasses import dataclass, field
from typing import TypeVar


def parse_lines(lines: List[str]) -> List[List[int]]:
    rows = []
    for line in lines:
        rows.append([int(c) for c in line])

    return rows


def visible_in_slice(this_tree: int, iy: int, slice: List[int]) -> bool:
    for ix, blocker in enumerate(slice):
        if blocker >= this_tree:
            # print(f"Tree at [{x},{y}] was blocked by tree at {ix}, {iy}")
            return False
    return True


def viewable_trees_in_slice(this_tree: int, slice: List[int]) -> int:
    # min_viewable = this_tree
    viewed = 0
    for candidate in slice:
        if candidate < this_tree:
            viewed += 1
        else:
            return viewed + 1
            min_viewable = candidate

    return viewed


def get_slices(trees: List[List[int]], y: int, x: int) -> List[List[int]]:
    left = trees[y][0:x]
    right = trees[y][x + 1 :]
    up = [trees[yval][x] for yval in range(y)]
    down = [trees[yval][x] for yval in range(y + 1, len(trees))]
    # all lists shall go from the tree outward
    left.reverse()
    up.reverse()
    return [left, right, up, down]


def is_visible(trees: List[List[int]], y: int, x: int) -> bool:
    this_tree = trees[y][x]
    slices = get_slices(trees, y, x)
    for iy, slice in enumerate(slices):
        if visible_in_slice(this_tree, iy, slice):
            return True

    # every slice blocked
    return False


def scenic_score(trees: List[List[int]], y: int, x: int) -> int:
    this_tree = trees[y][x]
    slices = get_slices(trees, y, x)
    slice_scores = [viewable_trees_in_slice(this_tree, slice) for slice in slices]
    scenic_score = functools.reduce(lambda a, b: a * b, slice_scores, 1)
    # print(f"tree {x},{y}")
    # print(f"slices: {slices}")
    # print(f"scores {slice_scores}")
    # print(scenic_score)
    return scenic_score


def part_one(lines):
    trees = parse_lines(lines)

    visible = 0
    for idx_y, row in enumerate(trees):
        for idx_x, tree in enumerate(row):
            if is_visible(trees, idx_y, idx_x):
                visible += 1

    # count visible trees
    return visible


def part_two(lines):
    trees = parse_lines(lines)
    max_score = 0
    scores = []
    for idx_y, row in enumerate(trees):
        for idx_x, tree in enumerate(row):
            max_score = max(max_score, scenic_score(trees, idx_y, idx_x))
    return max_score


def main():
    with open("day8_input.txt", "r") as file:
        lines = file.read().splitlines()
        print(part_one(lines))
        print(part_two(lines))


if __name__ == "__main__":
    main()
