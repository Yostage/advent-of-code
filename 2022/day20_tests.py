import functools
import itertools
import unittest
from typing import Iterator

from day20 import (
    MixableNumber,
    mix,
    parse_lines,
    part_one,
    part_two,
    printable_vals,
    verify_integrity,
)


class TestDay20(unittest.TestCase):

    example = """1
2
-3
3
-2
0
4"""

    def test_parse_lines(self):
        nums = parse_lines(self.example.splitlines())
        self.assertEqual(len(nums), 7)

    def test_equality(self):
        one = MixableNumber(0, 0)
        two = MixableNumber(0, 2)
        one_p = MixableNumber(0, 0)
        self.assertNotEqual(one, two)
        self.assertTrue(one is not one_p)
        self.assertTrue(one is one)

    def test_mix(self):
        nums = parse_lines(["1", "2", "3"])
        self.assertEqual(printable_vals(nums), "1, 2, 3")
        mix(nums[0], nums)
        verify_integrity(nums)
        self.assertEqual(printable_vals(nums), "2, 1, 3")

        nums = parse_lines(["3", "2", "1"])
        self.assertEqual(printable_vals(nums), "3, 2, 1")
        mix(nums[-1], nums)
        verify_integrity(nums)
        self.assertEqual(printable_vals(nums), "3, 1, 2")

        nums = parse_lines(["-1", "2", "3"])
        self.assertEqual(printable_vals(nums), "-1, 2, 3")
        mix(nums[0], nums)
        verify_integrity(nums)
        self.assertEqual(printable_vals(nums), "2, -1, 3")

        nums = parse_lines(["1", "1"])
        self.assertEqual(printable_vals(nums), "1, 1")
        mix(nums[0], nums)
        verify_integrity(nums)
        self.assertEqual(printable_vals(nums), "1, 1")

        nums = parse_lines(["1", "2", "3"])
        mix(nums[0], nums)
        verify_integrity(nums)
        self.assertEqual(printable_vals(nums), "2, 1, 3")

        nums = parse_lines(["3", "2", "3"])
        mix(nums[0], nums)
        verify_integrity(nums)
        self.assertEqual(printable_vals(nums), "2, 3, 3")

        nums = parse_lines(["5", "2", "3"])
        mix(nums[0], nums)
        verify_integrity(nums)
        self.assertEqual(printable_vals(nums), "2, 5, 3")

    def test_full_mix(self):
        nums = parse_lines(self.example.splitlines())
        for num in nums:
            mix(num, nums)

        self.assertEqual(printable_vals(nums), "-2, 1, 2, -3, 4, 0, 3")
        # we don't match their start point but we do match their ordering
        # self.assertEqual(printable_vals(nums), "1, 2, -3, 4, 0, 3, -2")

    def test_part_one(self):
        result = part_one(self.example.splitlines())
        self.assertEqual(result, 3)

    def test_part_two(self):
        result = part_two(self.example.splitlines())
        # self.assertEqual(result, xx)


if __name__ == "__main__":
    unittest.main()
