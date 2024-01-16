from enum import Enum
from functools import lru_cache
from typing import Dict, List

from util import Point2D

CharacterGrid2D = Dict[Point2D, str]


class Directions:
    UP = NORTH = (0, -1)
    DOWN = SOUTH = (0, 1)
    LEFT = WEST = (-1, 0)
    RIGHT = EAST = (1, 0)


orthogonal_adjacencies = [
    Directions.EAST,
    Directions.SOUTH,
    Directions.WEST,
    Directions.NORTH,
]


class CharacterGrid:
    map: CharacterGrid2D

    _max_x: int = -1
    _max_y: int = -1

    def __init__(self, map: CharacterGrid2D):
        self.map = map

    @staticmethod
    def from_lines(lines: List[str]) -> "CharacterGrid":
        return CharacterGrid(
            map={(x, y): c for y, line in enumerate(lines) for x, c in enumerate(line)}
        )

    @lru_cache
    def min_x(self) -> int:
        return min(pt[0] for pt in self.map.keys())

    @lru_cache
    def min_y(self) -> int:
        return min(pt[1] for pt in self.map.keys())

    @lru_cache
    def max_x(self) -> int:
        return max(pt[0] for pt in self.map.keys())

    @lru_cache
    def max_y(self) -> int:
        return max(pt[1] for pt in self.map.keys())

    def width(self) -> int:
        return 1 + self.max_x() - self.min_x()

    def height(self) -> int:
        return 1 + self.max_y() - self.min_y()

    def render(self) -> None:
        print()
        for y in range(self.min_y(), self.max_y() + 1):
            print(
                "".join(
                    [self.map[(x, y)] for x in range(self.min_x(), self.max_x() + 1)]
                )
            )
        print()
