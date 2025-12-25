import unittest

from day09 import parse_lines, part_one, part_two


class TestDay09(unittest.TestCase):
    example = """7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3"""

    def test_parse_lines(self):
        parse_lines(self.example.splitlines())

    def test_part_one(self):
        result = part_one(self.example.splitlines())
        self.assertEqual(result, 50)

    def test_part_two(self):
        result = part_two(self.example.splitlines())
        self.assertEqual(result, 24)


if __name__ == "__main__":
    unittest.main()
