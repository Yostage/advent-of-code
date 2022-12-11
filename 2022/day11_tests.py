import functools
import itertools
import unittest
from typing import Iterator

from day11 import parse_lines, part_one, part_two


class TestDay11(unittest.TestCase):

    example = """Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1
    """

    def test_parse_lines(self):
        print(parse_lines(self.example.splitlines()))

    def test_part_one(self):
        result = part_one(self.example.splitlines())
        self.assertEqual(result, 10605)

    def test_part_two(self):
        result = part_two(self.example.splitlines())
        self.assertEqual(result, 2713310158)


if __name__ == "__main__":
    unittest.main()
