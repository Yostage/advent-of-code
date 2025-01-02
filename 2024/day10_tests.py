import unittest

from day10 import parse_lines, part_one, part_two


class TestDay10(unittest.TestCase):
    example = """89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732"""

    def test_parse_lines(self):
        parse_lines(self.example.splitlines())

    def test_part_one(self):
        result = part_one(self.example.splitlines())
        self.assertEqual(result, 36)

    def test_part_two(self):
        result = part_two(self.example.splitlines())
        # self.assertEqual(result, xx)


if __name__ == "__main__":
    unittest.main()
