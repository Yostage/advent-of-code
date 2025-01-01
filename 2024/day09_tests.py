import unittest

from day09 import parse_lines, part_one, part_two


class TestDay09(unittest.TestCase):
    example = """2333133121414131402"""

    def test_parse_lines(self):
        parse_lines(self.example.splitlines())

    def test_part_one(self):
        result = part_one(self.example.splitlines())
        self.assertEqual(result, 1928)

    def test_part_two(self):
        result = part_two(self.example.splitlines())
        self.assertEqual(result, 2858)


if __name__ == "__main__":
    unittest.main()
