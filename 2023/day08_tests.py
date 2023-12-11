import functools
import itertools
import unittest
from typing import Iterator

from day08 import parse_lines, part_one, part_two


class TestDay08(unittest.TestCase):
    example = """RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)
"""

    example2 = """LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)"""

    def test_parse_lines(self):
        parse_lines(self.example.splitlines())

    def test_part_one(self):
        result = part_one(self.example.splitlines())
        self.assertEqual(result, 2)
        self.assertEqual(part_one(self.example2.splitlines()), 6)

    def test_part_two(self):
        result = part_two(self.example.splitlines())
        # self.assertEqual(result, xx)


if __name__ == "__main__":
    unittest.main()
