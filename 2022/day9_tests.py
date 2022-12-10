import functools
import itertools
import unittest
from typing import Iterator

from day9 import parse_lines, part_one, part_two


class TestDay9(unittest.TestCase):

    example = """R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2"""

    example2 = """R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20"""

    def test_parse_lines(self):
        input = parse_lines(self.example.splitlines())
        print(input)
        self.assertTrue(True)

    def test_part_one(self):
        result = part_one(self.example.splitlines())
        self.assertEqual(result, 13)

    def test_part_two(self):
        result = part_two(self.example2.splitlines())
        self.assertEqual(result, 36)


if __name__ == "__main__":
    unittest.main()
