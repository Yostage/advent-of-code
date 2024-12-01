import unittest

from day01 import parse_lines, part_one, part_two


class TestDay01(unittest.TestCase):
    example = """3   4
4   3
2   5
1   3
3   9
3   3"""

    def test_parse_lines(self):
        parse_lines(self.example.splitlines())

    def test_part_one(self):
        result = part_one(self.example.splitlines())
        self.assertEqual(result, 11)

    def test_part_two(self):
        result = part_two(self.example.splitlines())
        # self.assertEqual(result, xx)


if __name__ == "__main__":
    unittest.main()
