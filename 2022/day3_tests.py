import unittest

from day3 import char_to_priority, find_shared_priority


class TestDay3(unittest.TestCase):

    example = """vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw"""

    def test_example(self):
        pri = [find_shared_priority(sack) for sack in self.example.splitlines()]
        self.assertEqual(sum(pri), 157)

    def test_shared_priority(self):
        self.assertEqual(find_shared_priority("abbc"), 2)

    def test_priority(self):
        # Lowercase item types a through z have priorities 1 through 26.
        # Uppercase item types A through Z have priorities 27 through 52.

        self.assertEqual(char_to_priority("a"), 1)
        self.assertEqual(char_to_priority("z"), 26)
        self.assertEqual(char_to_priority("A"), 27)
        self.assertEqual(char_to_priority("Z"), 52)


if __name__ == "__main__":
    unittest.main()
