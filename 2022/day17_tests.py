import functools
import itertools
import unittest
from typing import Iterator

from more_itertools import first

from day17 import Rock, Tetris, parse_lines, part_one, part_two


class TestDay17(unittest.TestCase):

    example = """>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"""

    def test_pixel_collision(self):
        t = Tetris()
        r = Rock((5, 1), 0)
        self.assertFalse(r.test_all_empty(t, (0, 0)))

    def test_apply(self):
        r = Rock((0, 0), 0)
        self.assertEqual(first(r.all_pixels()), (0, 0))
        r.apply((10, 0))
        self.assertEqual(first(r.all_pixels()), (10, 0))

    def test_parse_lines(self):
        parse_lines(self.example.splitlines())

    def test_part_one(self):
        result = part_one(self.example.splitlines(), 1)
        self.assertEqual(result, 1)
        result = part_one(self.example.splitlines(), 2)
        self.assertEqual(result, 4)
        result = part_one(self.example.splitlines(), 3)
        self.assertEqual(result, 6)
        result = part_one(self.example.splitlines(), 4)
        self.assertEqual(result, 7)
        result = part_one(self.example.splitlines(), 5)
        self.assertEqual(result, 9)
        result = part_one(self.example.splitlines(), 6)
        self.assertEqual(result, 10)
        result = part_one(self.example.splitlines(), 7)
        self.assertEqual(result, 13)
        result = part_one(self.example.splitlines(), 8)
        self.assertEqual(result, 15)
        result = part_one(self.example.splitlines(), 9)
        self.assertEqual(result, 17)
        result = part_one(self.example.splitlines(), 10)
        self.assertEqual(result, 17)

        # result = part_one(self.example.splitlines())
        # self.assertEqual(result, 3068)
        pass

    def test_part_two(self):
        result = part_two(self.example.splitlines())
        # self.assertEqual(result, xx)


if __name__ == "__main__":
    unittest.main()
