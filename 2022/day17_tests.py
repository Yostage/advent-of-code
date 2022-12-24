import functools
import itertools
import unittest
from typing import Iterator

from more_itertools import first

from day17 import Rock, Tetris, parse_lines, part_one, part_one_generator, part_two


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
        self.assertListEqual(
            list(itertools.islice(part_one_generator(self.example.splitlines()), 11)),
            [0, 1, 4, 6, 7, 9, 10, 13, 15, 17, 17],
        )

        result = part_one(self.example.splitlines())
        self.assertEqual(result, 3068)

        pass

    def test_part_two(self):
        result = part_two(self.example.splitlines())
        self.assertEqual(result, 1514285714288)


if __name__ == "__main__":
    unittest.main()
