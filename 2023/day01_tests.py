import functools
import itertools
import unittest
from typing import Iterator

from day01 import parse_lines, part_one, part_two


class TestDay01(unittest.TestCase):
    example = """1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet"""

    example2 = """two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen"""

    def test_parse_lines(self):
        parse_lines(self.example.splitlines())

    def test_part_one(self):
        result = part_one(self.example.splitlines())
        self.assertEqual(result, 142)

    def test_part_two(self):
        result = part_two(self.example2.splitlines())
        self.assertEqual(result, 281)


if __name__ == "__main__":
    unittest.main()
