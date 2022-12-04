import unittest
from day2 import RPS, scoring, sum_score


class TestDay2(unittest.TestCase):
    def test_scoring(self):
        self.assertEqual(scoring(RPS.ROCK, RPS.ROCK), 3)
        self.assertEqual(scoring(RPS.ROCK, RPS.PAPER), 0)
        self.assertEqual(scoring(RPS.ROCK, RPS.SCISSORS), 6)
        self.assertEqual(scoring(RPS.SCISSORS, RPS.ROCK), 0)
        self.assertEqual(scoring(RPS.SCISSORS, RPS.PAPER), 6)
        self.assertEqual(scoring(RPS.SCISSORS, RPS.SCISSORS), 3)

    def test_example(self):
        example = """A Y
B X
C Z
"""

        self.assertEqual(sum_score(example.splitlines()), 15)


if __name__ == "__main__":
    unittest.main()
