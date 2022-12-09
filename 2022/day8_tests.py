import functools
import itertools
import unittest
from typing import Iterator

from day8 import parse_lines, part_one, part_two


class TestDay8(unittest.TestCase):

    example = """30373
25512
65332
33549
35390"""

    def test_parse_lines(self):
        parse_lines(self.example.splitlines())
        self.assertTrue(True)

    def test_part_one(self):
        trees = parse_lines(self.example.splitlines())
        self.assertEqual(part_one(self.example.splitlines()), 21)
        # self.assertTrue(True)

    def test_part_two(self):
        self.assertEqual(part_two(self.example.splitlines()), 8)
        # self.assertTrue(True)


if __name__ == "__main__":
    unittest.main()
