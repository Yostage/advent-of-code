import functools
import itertools
import unittest
from typing import Iterator

from day24 import parse_lines, part_one, part_two


class TestDay24(unittest.TestCase):

    example = """#.#####
#.....#
#>....#
#.....#
#...v.#
#.....#
#####.#"""

    example2 = """#.######
#>>.<^<#
#.<..<<#
#>v.><>#
#<^v^^>#
######.#"""

    def test_parse_lines(self):
        parse_lines(self.example.splitlines())

    def test_part_one(self):
        result = part_one(self.example2.splitlines())
        self.assertEqual(result, 18)

    def test_part_two(self):
        result = part_two(self.example2.splitlines())
        self.assertEqual(result, 54)


if __name__ == "__main__":
    unittest.main()
