import functools
import itertools
import unittest
from typing import Iterator

from day14 import parse_lines, part_one, part_two


class TestDay14(unittest.TestCase):

    example = """498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9"""

    def test_parse_lines(self):
        parse_lines(self.example.splitlines())

    def test_part_one(self):
        result = part_one(self.example.splitlines())
        self.assertEqual(result, 24)

    def test_part_two(self):
        result = part_two(self.example.splitlines())
        # self.assertEqual(result, 21)


if __name__ == "__main__":
    unittest.main()
