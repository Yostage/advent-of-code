import functools
import itertools
import unittest
from typing import Iterator

from day25 import parse_lines, part_one, part_two


class TestDay25(unittest.TestCase):

    example = """1=-0-2
12111
2=0=
21
2=01
111
20012
112
1=-1=
1-12
12
1=
122"""

    def test_parse_lines(self):
        parse_lines(self.example.splitlines())

    def test_part_one(self):
        result = part_one(self.example.splitlines())
        # self.assertEqual(result, xx)

    def test_part_two(self):
        result = part_two(self.example.splitlines())
        # self.assertEqual(result, xx)


if __name__ == "__main__":
    unittest.main()
