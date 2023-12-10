import functools
import itertools
import unittest
from typing import Iterator

from day06 import parse_lines, part_one, part_two


class TestDay06(unittest.TestCase):
    example = """Time:      7  15   30
Distance:  9  40  200"""

    def test_parse_lines(self):
        parse_lines(self.example.splitlines())

    def test_part_one(self):
        result = part_one(self.example.splitlines())
        self.assertEqual(result, 288)

    def test_part_two(self):
        result = part_two(self.example.splitlines())
        # self.assertEqual(result, xx)


if __name__ == "__main__":
    unittest.main()
