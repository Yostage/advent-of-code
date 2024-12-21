import unittest

from day03 import parse_lines, part_one, part_two


class TestDay03(unittest.TestCase):
    example = (
        """xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"""
    )
    example2 = (
        """xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"""
    )

    def test_parse_lines(self):
        parse_lines(self.example.splitlines())

    def test_part_one(self):
        result = part_one(self.example.splitlines())
        self.assertEqual(result, 161)

    def test_part_two(self):
        result = part_two(self.example2.splitlines())
        self.assertEqual(result, 48)


if __name__ == "__main__":
    unittest.main()
