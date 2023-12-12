import functools
import itertools
import unittest
from typing import Iterator

from day09 import parse_lines, part_one, part_two


class TestDay09(unittest.TestCase):
    example = """0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45"""

    def test_parse_lines(self):
        parse_lines(self.example.splitlines())

    def test_part_one(self):
        result = part_one(self.example.splitlines())
        self.assertEqual(result, 114)

    def test_part_two(self):
        result = part_two(self.example.splitlines())
        self.assertEqual(result, 2)


if __name__ == "__main__":
    unittest.main()
