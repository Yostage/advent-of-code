import unittest

from day01 import parse_lines, part_one, part_two, part_two_impl


class TestDay01(unittest.TestCase):
    example = """L68
L30
R48
L5
R60
L55
L1
L99
R14
L82"""

    def test_parse_lines(self):
        parse_lines(self.example.splitlines())

    def test_part_one(self):
        result = part_one(self.example.splitlines())
        self.assertEqual(result, 3)

    def test_part_two(self):
        result = part_two(self.example.splitlines())

        self.assertEqual(part_two_impl(95, 10), (5, 1))
        self.assertEqual(part_two_impl(95, 110), (5, 2))
        self.assertEqual(part_two_impl(5, -5), (0, 1))
        self.assertEqual(part_two_impl(5, -105), (0, 2))
        self.assertEqual(part_two_impl(5, -6), (99, 1))
        self.assertEqual(part_two_impl(0, -1), (99, 0))
        self.assertEqual(part_two_impl(0, 100), (0, 1))
        self.assertEqual(part_two_impl(0, 101), (1, 1))
        self.assertEqual(part_two_impl(0, -100), (0, 1))
        self.assertEqual(result, 6)


if __name__ == "__main__":
    unittest.main()
