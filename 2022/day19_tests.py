import functools
import itertools
import unittest
from typing import Iterator

from day19 import find_max_score, parse_lines, part_one, part_two, simulate


class TestDay19(unittest.TestCase):

    example = """Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.
Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian."""

    def test_parse_lines(self):
        parse_lines(self.example.splitlines())

    def test_simulate_example(self):
        bps = parse_lines(self.example.splitlines())
        # example_solution = "..c.c.c...zc..z..g..g..."
        # geodes = simulate(solution=example_solution, bp=bps[0], minutes=24)
        # self.assertEqual(geodes, 9)
        # wtf_solution = "...occcc.zc.zogczgzgzgg."
        # geodes = simulate(solution=wtf_solution, bp=bps[1], minutes=24)
        # self.assertEqual(geodes, 22)

    def test_find_max_score(self):
        bps = parse_lines(self.example.splitlines())
        # pass
        self.assertEqual(find_max_score(bps[0], 24), 9)
        self.assertEqual(find_max_score(bps[1], 24), 12)

    def test_part_one(self):
        return
        result = part_one(self.example.splitlines())
        self.assertEqual(result, 33)

    def test_part_two(self):
        result = part_two(self.example.splitlines())
        # self.assertEqual(result, xx)


if __name__ == "__main__":
    unittest.main()
