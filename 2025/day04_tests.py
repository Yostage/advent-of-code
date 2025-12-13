import unittest

from day04 import parse_lines, part_one, part_two


class TestDay04(unittest.TestCase):
    example = """..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@.
"""

    def test_parse_lines(self):
        parse_lines(self.example.splitlines())

    def test_part_one(self) -> None:
        result = part_one(self.example.splitlines())
        self.assertEqual(result, 13)

    def test_part_two(self):
        result = part_two(self.example.splitlines())
        # self.assertEqual(result, xx)


if __name__ == "__main__":
    unittest.main()
