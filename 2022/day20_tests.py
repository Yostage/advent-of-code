import functools
import itertools
import unittest
from typing import Iterator

from day20 import parse_lines, part_one, part_two


class TestDay20(unittest.TestCase):

    example = """1
2
-3
3
-2
0
4"""

    def test_parse_lines(self):
        parse_lines(self.example.splitlines())

    def test_part_one(self):
        result = part_one(self.example.splitlines())
        # self.assertEqual(result, xx)

    def test_part_two(self):
        result = part_two(self.example.splitlines())
        # self.assertEqual(result, xx)


if __name__ == "__main__":
    unittest.main()
