import unittest
from day2 import RPS, scoring, sum_score_v1, sum_score_v2


class TestDay2(unittest.TestCase):
    def test_scoring(self):
        self.assertEqual(scoring(RPS.ROCK, RPS.ROCK), 3)
        self.assertEqual(scoring(RPS.ROCK, RPS.PAPER), 0)
        self.assertEqual(scoring(RPS.ROCK, RPS.SCISSORS), 6)
        self.assertEqual(scoring(RPS.SCISSORS, RPS.ROCK), 0)
        self.assertEqual(scoring(RPS.SCISSORS, RPS.PAPER), 6)
        self.assertEqual(scoring(RPS.SCISSORS, RPS.SCISSORS), 3)

    example = """A Y
B X
C Z
"""

    def test_example_v1(self):
        self.assertEqual(sum_score_v1(self.example.splitlines()), 15)

    def test_example_v2(self):
        self.assertEqual(sum_score_v2(self.example.splitlines()), 12)


if __name__ == "__main__":
    unittest.main()
