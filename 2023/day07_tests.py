import functools
import itertools
import unittest
from typing import Iterator

from day07 import parse_lines, part_one, part_two


class TestDay07(unittest.TestCase):
    example = """32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483"""

    def test_parse_lines(self):
        parse_lines(self.example.splitlines())

    def test_part_one(self):
        result = part_one(self.example.splitlines())
        self.assertEqual(result, 6440)

    def test_part_two(self):
        result = part_two(self.example.splitlines())
        self.assertEqual(result, 5905)


if __name__ == "__main__":
    unittest.main()
