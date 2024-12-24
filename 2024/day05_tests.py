import unittest

from day05 import parse_lines, part_one, part_two


class TestDay05(unittest.TestCase):
    example = """47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47"""

    def test_parse_lines(self):
        parse_lines(self.example.splitlines())

    def test_part_one(self):
        result = part_one(self.example.splitlines())
        self.assertEqual(result, 143)

    def test_part_two(self):
        result = part_two(self.example.splitlines())
        self.assertEqual(result, 123)


if __name__ == "__main__":
    unittest.main()
