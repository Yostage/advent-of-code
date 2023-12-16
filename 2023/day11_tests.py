import functools
import itertools
import unittest
from typing import Iterator

from day11 import calculate_distances, parse_lines, part_one, part_two


class TestDay11(unittest.TestCase):
    example = """...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#....."""

    def test_parse_lines(self):
        parse_lines(self.example.splitlines())

    def test_part_one(self):
        result = part_one(self.example.splitlines())
        self.assertEqual(result, 374)

    def test_part_two(self):
        galaxies = parse_lines(self.example.splitlines())
        self.assertEqual(calculate_distances(galaxies, 9), 1030)
        self.assertEqual(calculate_distances(galaxies, 99), 8410)


if __name__ == "__main__":
    unittest.main()
