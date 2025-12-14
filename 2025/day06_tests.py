import unittest

from day06 import parse_lines, part_one, part_two


class TestDay06(unittest.TestCase):
    example = """123 328  51 64 
 45 64  387 23 
  6 98  215 314
*   +   *   +  """

    def test_parse_lines(self):
        parse_lines(self.example.splitlines())

    def test_part_one(self):
        result = part_one(self.example.splitlines())
        self.assertEqual(result, 4277556)

    def test_part_two(self):
        result = part_two(self.example.splitlines())
        # self.assertEqual(result, xx)


if __name__ == "__main__":
    unittest.main()
