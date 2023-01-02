import functools
import itertools
import unittest
from typing import Iterator

from day23 import parse_lines, part_one, part_two


class TestDay23(unittest.TestCase):

    example = """.....
..##.
..#..
.....
..##.
....."""

    example2 = """....#..
..###.#
#...#.#
.#...##
#.###..
##.#.##
.#..#.."""

    def test_parse_lines(self):
        parse_lines(self.example.splitlines())

    def test_part_one(self):
        result = part_one(self.example2.splitlines())
        self.assertEqual(result, 110)

    def test_part_two(self):
        # pass
        result = part_two(self.example2.splitlines())
        self.assertEqual(result, 20)


if __name__ == "__main__":
    unittest.main()
