import functools
import itertools
import unittest
from typing import Iterator

from day15 import parse_lines, part_one, part_two


class TestDay15(unittest.TestCase):
    example = """rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"""

    def test_parse_lines(self):
        parse_lines(self.example.splitlines())

    def test_part_one(self):
        result = part_one(self.example.splitlines())
        self.assertEqual(result, 1320)

    def test_part_two(self):
        result = part_two(self.example.splitlines())
        self.assertEqual(result, 145)


if __name__ == "__main__":
    unittest.main()
