import functools
import itertools
import unittest
from textwrap import dedent
from typing import Iterator

from day10 import parse_lines, part_one, part_two


class TestDay10(unittest.TestCase):
    example = """.....
.S-7.
.|.|.
.L-J.
.....
"""
    example2 = """..F7.
.FJ|.
SJ.L7
|F--J
LJ..."""

    example3 = dedent(
        """\
...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
..........."""
    )

    example4 = dedent(
        """\
..........
.S------7.
.|F----7|.
.||....||.
.||....||.
.|L-7F-J|.
.|..||..|.
.L--JL--J.
.........."""
    )

    example5 = dedent(
        """\
.F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ..."""
    )

    example6 = dedent(
        """\
FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L"""
    )

    example7 = dedent(
        """\
..F7..
F-JL-7
|....|
L-S--J"""
    )

    example8 = dedent(
        """\
F--7F--7
|F-JL-7|
||....||
|L----J|
L--S---J"""
    )

    def test_parse_lines(self):
        parse_lines(self.example.splitlines())

    def test_part_one(self):
        result = part_one(self.example.splitlines())
        self.assertEqual(result, 4)
        self.assertEqual(part_one(self.example2.splitlines()), 8)

    def test_part_two(self):
        # self.assertEqual(part_two(self.example3.splitlines()), 4)
        # self.assertEqual(part_two(self.example4.splitlines()), 4)
        # self.assertEqual(part_two(self.example5.splitlines()), 8)
        # self.assertEqual(part_two(self.example6.splitlines()), 10)
        self.assertEqual(part_two(self.example7.splitlines()), 10)
        self.assertEqual(part_two(self.example8.splitlines()), 4)


if __name__ == "__main__":
    unittest.main()
