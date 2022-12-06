import functools
import itertools
import unittest
from typing import Iterator

from day6 import find_signal


class TestDay6(unittest.TestCase):

    example1 = """bvwbjplbgvbhsrlpgdmjqwftvncz"""

    def test_part_one(self):
        self.assertEqual(find_signal(self.example1), 5)

    def test_part_two(self):
        self.assertEqual(find_signal(self.example1, 14), 23)


if __name__ == "__main__":
    unittest.main()
