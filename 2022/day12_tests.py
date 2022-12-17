import functools
import itertools
import unittest
from typing import Iterator

from day12 import parse_lines, part_one, part_two


class TestDay12(unittest.TestCase):

    example = """Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi"""

    def test_parse_lines(self):
        parse_lines(self.example.splitlines())

    def test_part_one(self):
        result = part_one(self.example.splitlines())
        self.assertEqual(result, 31)

    def test_part_two(self):
        result = part_two(self.example.splitlines())
        self.assertEqual(result, 29)
        pass


if __name__ == "__main__":
    unittest.main()
