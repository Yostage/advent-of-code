import unittest

from day05 import parse_lines, part_one, part_two


class TestDay05(unittest.TestCase):
    example = """3-5
10-14
16-20
12-18

1
5
8
11
17
32"""

    def test_parse_lines(self):
        parse_lines(self.example.splitlines())

    def test_part_one(self):
        result = part_one(self.example.splitlines())
        self.assertEqual(result, 3)

    def test_part_two(self):
        result = part_two(self.example.splitlines())
        self.assertEqual(result, 14)


if __name__ == "__main__":
    unittest.main()
