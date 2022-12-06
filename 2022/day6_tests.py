import functools
import itertools
from typing import Iterator
import unittest

from day5 import (
    cratelines_to_crates,
    parse_crateline,
    parse_input,
    parse_instructions,
    part_one,
    part_two,
    # input_string_to_intervals,
    # compare_intervals,
    # intervals_completely_overlap,
    # intervals_overlap,
)


class TestDay6(unittest.TestCase):

    example1 = """bvwbjplbgvbhsrlpgdmjqwftvncz"""

    def test_find_signal(self):
        def find_signal(line: str):
            # base case
            chars = list(line)
            buffer = chars[0:4]
            marker = 4
            del chars[0:4]
            for c in chars:
                if len(set(buffer)) == 4:
                    return marker
                del buffer[0]
                buffer += c
                marker += 1

            assert False

        self.assertEqual(find_signal(self.example1), 5)
        # shift

    # def test_part_one(self):
    #     answer = part_one(self.example.splitlines())
    #     self.assertEqual(answer, ["C", "M", "Z"])

    # def test_part_two(self):
    #     answer = part_two(self.example.splitlines())
    #     self.assertEqual(answer, ["M", "C", "D"])


if __name__ == "__main__":
    unittest.main()
