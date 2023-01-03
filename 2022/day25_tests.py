import functools
import itertools
import unittest
from typing import Iterator

from day25 import int_to_snafu, parse_lines, part_one, snafu_to_int


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

    examples = [
        (1, "1"),
        (2, "2"),
        (5, "10"),
        (10, "20"),
        (2022, "1=11-2"),
        (12345, "1-0---0"),
        (314159265, "1121-1110-1=0"),
    ]

    def test_int_to_snafu(self):
        for (integer, snafu) in self.examples:
            self.assertEqual(snafu, int_to_snafu(integer))

    def test_snafu_to_int(self):
        for (integer, snafu) in self.examples:
            self.assertEqual(integer, snafu_to_int(snafu))

    def test_part_one(self):
        result = part_one(self.example.splitlines())
        self.assertEqual(result, "2=-1=0")


if __name__ == "__main__":
    unittest.main()
