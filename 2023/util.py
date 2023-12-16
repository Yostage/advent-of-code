# 2022.15
from typing import Tuple

Point2D = Tuple[int, int]


# 2022.22
def tuple2_add(a: Point2D, b: Point2D) -> Point2D:
    return tuple(map(sum, zip(a, b)))  # type: ignore


# 2022.15
def manhattan_distance(a: Point2D, b: Point2D) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])
