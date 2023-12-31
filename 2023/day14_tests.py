import functools
import itertools
import unittest
from typing import Iterator

from day14 import parse_lines, part_one, part_two


class TestDay14(unittest.TestCase):
    example = """O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#...."""

    def test_parse_lines(self):
        parse_lines(self.example.splitlines())

    def test_part_one(self):
        result = part_one(self.example.splitlines())
        self.assertEqual(result, 136)

    def test_part_two(self):
        result = part_two(self.example.splitlines())
        self.assertEqual(result, 64)


if __name__ == "__main__":
    unittest.main()
