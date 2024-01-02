from functools import lru_cache
from typing import Dict, List

from util import Point2D

CharacterGrid2D = Dict[Point2D, str]


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
