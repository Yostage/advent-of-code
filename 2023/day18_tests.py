import functools
import itertools
import unittest
from typing import Iterator

from day18 import parse_lines, part_one, part_two


class TestDay18(unittest.TestCase):
    example = """R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)
"""

    example2 = """R 6 (#70c710)
D 4 (#0dc571)
L 2 (#5713f0)
U 2 (#d2c081)
L 2 (#59c680)
D 4 (#411b91)
L 2 (#8ceee2)
U 6 (#caa173)
"""

    example3 = """D 4 (#70c710)
R 6 (#0dc571)
U 6 (#5713f0)
L 2 (#59c680)
D 4 (#411b91)
L 2 (#8ceee2)
U 2 (#8ceee2)
L 2 (#8ceee2)
"""

    def test_parse_lines(self):
        parse_lines(self.example.splitlines())

    def test_part_one(self):
        result = part_one(self.example.splitlines())
        self.assertEqual(result, 62)
        result = part_one(self.example2.splitlines())
        self.assertEqual(result, 39)
        result = part_one(self.example3.splitlines())
        self.assertEqual(result, 39)

    def test_part_two(self):
        result = part_two(self.example.splitlines())
        self.assertEqual(result, 952408144115)
        result = part_two(self.example.splitlines(), legacy=True)
        self.assertEqual(result, 62)
        result = part_two(self.example2.splitlines(), legacy=True)
        self.assertEqual(result, 39)
        result = part_two(self.example3.splitlines(), legacy=True)
        self.assertEqual(result, 39)


if __name__ == "__main__":
    unittest.main()
