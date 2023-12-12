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

    example3 = """LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)"""

    def test_parse_lines(self):
        parse_lines(self.example.splitlines())

    def test_part_one(self):
        result = part_one(self.example.splitlines())
        self.assertEqual(result, 2)
        self.assertEqual(part_one(self.example2.splitlines()), 6)

    def test_part_two(self):
        result = part_two(self.example3.splitlines())
        self.assertEqual(result, 6)


if __name__ == "__main__":
    unittest.main()
