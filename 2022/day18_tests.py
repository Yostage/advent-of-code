import functools
import itertools
import unittest
from typing import Iterator

from day18 import parse_lines, part_one, part_two


class TestDay18(unittest.TestCase):

    baby_example = """1,1,1
2,1,1"""
    example = """2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5"""

    def test_parse_lines(self):
        parse_lines(self.example.splitlines())

    def test_part_one(self):
        result = part_one(self.baby_example.splitlines())
        self.assertEqual(result, 10)

        result = part_one(self.example.splitlines())
        self.assertEqual(result, 64)

    def test_part_two(self):
        result = part_two(self.example.splitlines())
        self.assertEqual(result, 58)


if __name__ == "__main__":
    unittest.main()
