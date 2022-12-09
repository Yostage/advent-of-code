import functools
import itertools
import unittest
from typing import Iterator

from day9 import parse_lines, part_one, part_two


class TestDay9(unittest.TestCase):

    example = """
    """

    def test_parse_lines(self):
        parse_lines(self.example.splitlines())
        self.assertTrue(True)

    def test_part_one(self):
        # self.assertEqual(part_one(self.example.splitlines()), 21)
        self.assertTrue(True)

    def test_part_two(self):
        # self.assertEqual(part_two(self.example.splitlines()), 8)
        self.assertTrue(True)


if __name__ == "__main__":
    unittest.main()
