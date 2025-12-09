import unittest

from day02 import parse_lines, part_one, part_two


class TestDay02(unittest.TestCase):
    example = """11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124"""

    def test_parse_lines(self):
        parse_lines(self.example.splitlines())

    def test_part_one(self):
        result = part_one(self.example.splitlines())
        self.assertEqual(result, 1227775554)

    def test_part_two(self):
        result = part_two(self.example.splitlines())
        self.assertEqual(result, 4174379265)


if __name__ == "__main__":
    unittest.main()
