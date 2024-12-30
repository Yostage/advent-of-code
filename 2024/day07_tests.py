import unittest

from day07 import parse_lines, part_one, part_two


class TestDay07(unittest.TestCase):
    example = """190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20"""

    def test_parse_lines(self):
        parse_lines(self.example.splitlines())

    def test_part_one(self):
        result = part_one(self.example.splitlines())
        self.assertEqual(result, 3749)

    def test_part_two(self):
        result = part_two(self.example.splitlines())
        self.assertEqual(result, 11387)


if __name__ == "__main__":
    unittest.main()
