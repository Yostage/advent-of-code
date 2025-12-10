import unittest

from day03 import parse_lines, part_one, part_two


class TestDay03(unittest.TestCase):
    example = """987654321111111
811111111111119
234234234234278
818181911112111"""

    def test_parse_lines(self):
        parse_lines(self.example.splitlines())

    def test_part_one(self):
        result = part_one(self.example.splitlines())
        self.assertEqual(result, 357)

    def test_part_two(self):
        result = part_two(self.example.splitlines())
        # self.assertEqual(result, xx)


if __name__ == "__main__":
    unittest.main()
