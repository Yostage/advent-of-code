import functools
import itertools
from typing import Iterator
import unittest

from day4 import (
    input_string_to_intervals,
    compare_intervals,
    intervals_completely_overlap,
    intervals_overlap,
)


class TestDay4(unittest.TestCase):

    example = """2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8"""

    def test_example1(self):
        intervalList = [
            input_string_to_intervals(line) for line in self.example.splitlines()
        ]
        matches = [1 if intervals_completely_overlap(i) else 0 for i in intervalList]
        self.assertEqual(sum(matches), 2)

    def test_input_parsing(self):
        l1 = self.example.splitlines()[0]
        self.assertEqual(input_string_to_intervals(l1), [[2, 4], [6, 8]])

    def test_compare_intervals(self):
        self.assertEqual(compare_intervals([1, 2], [1, 2]), 0)
        self.assertLess(compare_intervals([1, 2], [2, 3]), 0)
        self.assertLess(compare_intervals([1, 3], [1, 2]), 0)

    def test_sort_intervals(self):
        self.assertListEqual(
            sorted([[5, 6], [2, 3]], key=functools.cmp_to_key(compare_intervals)),
            [[2, 3], [5, 6]],
        )

        self.assertListEqual(
            sorted([[1, 2], [1, 3]], key=functools.cmp_to_key(compare_intervals)),
            [[1, 3], [1, 2]],
        )

    def test_intervals_completely_overlap(self):
        self.assertTrue(intervals_completely_overlap([[1, 2], [1, 3]]))
        self.assertFalse(intervals_completely_overlap([[1, 2], [2, 3]]))
        self.assertFalse(intervals_completely_overlap([[1, 3], [2, 4]]))

    def test_intervals_overlap(self):
        self.assertTrue(intervals_overlap([[1, 2], [1, 2]]))
        self.assertTrue(intervals_overlap([[1, 2], [2, 3]]))
        self.assertTrue(intervals_overlap([[1, 3], [2, 4]]))
        self.assertFalse(intervals_overlap([[1, 3], [4, 5]]))


if __name__ == "__main__":
    unittest.main()
