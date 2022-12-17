import functools
import itertools
import unittest
from typing import Iterator

from day13 import compare, parse_lines, part_one, part_two


class TestDay13(unittest.TestCase):

    example = """[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]"""

    def test_parse_lines(self):
        parse_lines(self.example.splitlines())

    def test_part_one(self):
        result = part_one(self.example.splitlines())
        self.assertEqual(result, 13)

    def test_part_two(self):
        result = part_two(self.example.splitlines())
        # self.assertEqual(result, 21)

    def test_compare(self):
        self.assertEqual(compare(1, 3), -1)
        self.assertEqual(compare([1, 1, 3, 1, 1], [1, 1, 5, 1, 1]), -1)
        self.assertEqual(compare([[1], [2, 3, 4]], [[1], 4]), -1)
        self.assertEqual(compare([[4, 4], 4, 4], [[4, 4], 4, 4, 4]), -1)
        self.assertEqual(compare([7, 7, 7, 7], [7, 7, 7]), 1)
        self.assertEqual(compare([], [3]), -1)
        self.assertEqual(compare([], [3]), -1)
        self.assertEqual(compare([[[]]], [[]]), 1)
        self.assertEqual(
            compare(
                [1, [2, [3, [4, [5, 6, 7]]]], 8, 9], [1, [2, [3, [4, [5, 6, 0]]]], 8, 9]
            ),
            1,
        )


if __name__ == "__main__":
    unittest.main()
