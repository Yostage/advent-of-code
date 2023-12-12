import functools
import itertools
import unittest
from typing import Iterator

from day10 import parse_lines, part_one, part_two


class TestDay10(unittest.TestCase):
    example = """.....
.S-7.
.|.|.
.L-J.
.....
"""
    example2 = """..F7.
.FJ|.
SJ.L7
|F--J
LJ..."""

    def test_parse_lines(self):
        parse_lines(self.example.splitlines())

    def test_part_one(self):
        result = part_one(self.example.splitlines())
        self.assertEqual(result, 4)
        self.assertEqual(part_one(self.example2.splitlines()), 8)

    def test_part_two(self):
        result = part_two(self.example.splitlines())
        # self.assertEqual(result, xx)


if __name__ == "__main__":
    unittest.main()
