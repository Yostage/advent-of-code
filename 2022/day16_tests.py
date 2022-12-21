import functools
import itertools
import unittest
from typing import Iterator

# part_two,
from day16 import parse_lines  # adjacent_candidates,
from day16 import bfs_shortest_distance, part_one, simulate_solution


class TestDay16(unittest.TestCase):

    example = """Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II"""

    example2 = """Valve AA has flow rate=0; tunnels lead to valves BB2, CC2
    Valve BB2 has flow rate=1; tunnels lead to valves AA, CC2
    Valve CC2 has flow rate=2; tunnels lead to valves AA, BB2"""

    example3 = """Valve AA has flow rate=0; tunnels lead to valves BB3, CC3
    Valve BB3 has flow rate=0; tunnels lead to valves AA, DD3
    Valve CC3 has flow rate=1; tunnels lead to valves AA
    Valve DD3 has flow rate=20; tunnels lead to valves BB3"""

    def test_parse_lines(self):
        valves = parse_lines(self.example.splitlines())
        # for v in valves.values():
        #     print(f"Valve {v.name} flow rate {v.flow_rate}")

    def test_bfs_distance(self):
        valves = parse_lines(self.example.splitlines())
        self.assertEqual(bfs_shortest_distance(valves, start_at="AA", dest="BB"), 1)
        self.assertEqual(bfs_shortest_distance(valves, start_at="AA", dest="DD"), 1)
        self.assertEqual(bfs_shortest_distance(valves, start_at="AA", dest="JJ"), 2)

    def test_examples(self):
        self.assertEqual(part_one(self.example2.splitlines(), days_total=1)[0], 0)
        self.assertEqual(part_one(self.example2.splitlines(), days_total=2)[0], 0)
        self.assertEqual(part_one(self.example2.splitlines(), days_total=3)[0], 2)
        self.assertEqual(part_one(self.example2.splitlines(), days_total=4)[0], 4)
        self.assertEqual(part_one(self.example2.splitlines(), days_total=5)[0], 7)

        result = part_one(self.example3.splitlines(), days_total=1)
        self.assertEqual(part_one(self.example3.splitlines(), days_total=1)[0], 0)
        self.assertEqual(part_one(self.example3.splitlines(), days_total=2)[0], 0)
        self.assertEqual(part_one(self.example3.splitlines(), days_total=3)[0], 1)
        # here the strategy can afford to shift
        self.assertEqual(part_one(self.example3.splitlines(), days_total=4)[0], 20)
        self.assertEqual(part_one(self.example3.splitlines(), days_total=5)[0], 40)

    def test_simulate_solution(self):
        canonical_solution = ["AA", "DD", "BB", "JJ", "HH", "EE", "CC"]
        valves = parse_lines(self.example.splitlines())
        self.assertEqual(
            simulate_solution(
                valves,
                canonical_solution,
                30,
                verbose=True,
            ),
            1651,
        )

    def test_part_one(self):
        valves = parse_lines(self.example.splitlines())
        self.assertEqual(part_one(self.example.splitlines(), days_total=3)[0], 20)
        result = part_one(self.example.splitlines(), days_total=3)
        self.assertEqual(result[0], 20)

        print(result[1])
        self.assertEqual(result[0], 1651)

    # def test_part_two(self):
    #     result = part_two(self.example.splitlines())
    # self.assertEqual(result, 21)


if __name__ == "__main__":
    unittest.main()
