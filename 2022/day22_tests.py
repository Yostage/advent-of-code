import functools
import itertools
import unittest
from typing import Iterator

from day22 import parse_lines, part_one, part_two


class TestDay22(unittest.TestCase):

    example = """        ...#
        .#..
        #...
        ....
...#.......#
........#...
..#....#....
..........#.
        ...#....
        .....#..
        .#......
        ......#.

10R5L5R10L4R5L5"""

    def test_parse_lines(self):
        pac = parse_lines(self.example.splitlines())
        pac.render_quadrants()

    def test_part_one(self):
        result = part_one(self.example.splitlines())
        self.assertEqual(result, 6032)

    def test_edge_traversal(self):
        pac = parse_lines(self.example.splitlines())

        # 4 -> 6 (A)
        pac.loc = (11, 5)
        pac._rotate_to_facing((1, 0))
        pac.step_one_cube_rules()
        self.assertEqual(pac.facing, (0, 1))
        self.assertEqual(pac.loc, (14, 8))
        pac.turn_left()
        pac.turn_left()
        pac.step_one_cube_rules()
        self.assertEqual(pac.facing, (-1, 0))
        self.assertEqual(pac.loc, (11, 5))

        # 5 -> 2 (F)
        pac.loc = (8, 11)
        pac._rotate_to_facing((0, 1))
        pac.step_one_cube_rules()
        self.assertEqual(pac.facing, (0, -1))
        self.assertEqual(pac.loc, (3, 7))
        pac.turn_left()
        pac.turn_left()
        pac.step_one_cube_rules()
        self.assertEqual(pac.facing, (0, -1))
        self.assertEqual(pac.loc, (8, 11))

        # 3 -> 1 (B)
        pac.loc = (4, 4)
        pac._rotate_to_facing((0, -1))
        pac.step_one_cube_rules()
        self.assertEqual(pac.facing, (1, 0))
        self.assertEqual(pac.loc, (8, 0))
        pac.turn_left()
        pac.turn_left()
        pac.step_one_cube_rules()
        self.assertEqual(pac.facing, (0, 1))
        self.assertEqual(pac.loc, (4, 4))

        # 1 -> 6 (D)
        pac.loc = (11, 1)
        pac._rotate_to_facing((1, 0))
        pac.step_one_cube_rules()
        self.assertEqual(pac.facing, (-1, 0))
        self.assertEqual(pac.loc, (15, 10))
        pac.turn_left()
        pac.turn_left()
        pac.step_one_cube_rules()
        self.assertEqual(pac.facing, (-1, 0))
        self.assertEqual(pac.loc, (11, 1))

    def test_part_two(self):
        result = part_two(self.example.splitlines())
        self.assertEqual(result, 5031)


if __name__ == "__main__":
    unittest.main()
