import functools
import itertools
from typing import Iterator
import unittest

from day5 import (
    parse_crateline,
    parse_input,
    parse_instructions,
    # input_string_to_intervals,
    # compare_intervals,
    # intervals_completely_overlap,
    # intervals_overlap,
)


class TestDay5(unittest.TestCase):

    example = """    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2"""

    def test_parse_crateline(self):
        self.assertEqual(parse_crateline("[N] [C]"), ["N", "C"])
        self.assertEqual(parse_crateline("        [D]"), [None, None, "D"])

    def test_parse_instructions(self):
        self.assertEqual(parse_instructions("move 1 from 2 to 1"), [1, 2, 1])
        self.assertEqual(parse_instructions("move 1 from 1 to 2"), [1, 1, 2])

    def test_parse_example(self):
        (top_down_crates, moves) = parse_input(self.example.splitlines())
        self.assertEqual(
            top_down_crates, [[None, "D", None], ["N", "C", None], ["Z", "M", "P"]]
        )
        self.assertEqual(moves, [[1, 2, 1], [3, 1, 3], [2, 2, 1], [1, 1, 2]])


if __name__ == "__main__":
    unittest.main()
