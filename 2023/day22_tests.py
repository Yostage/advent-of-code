import unittest

from day22 import parse_lines, part_one, part_two


class TestDay22(unittest.TestCase):
    example = """1,0,1~1,2,1
0,0,2~2,0,2
0,2,3~2,2,3
0,0,4~0,2,4
2,0,5~2,2,5
0,1,6~2,1,6
1,1,8~1,1,9"""

    def test_parse_lines(self):
        parse_lines(self.example.splitlines())

    def test_part_one(self):
        result = part_one(self.example.splitlines())
        self.assertEqual(result, 5)

    def test_part_two(self):
        result = part_two(self.example.splitlines())
        self.assertEqual(result, 7)


if __name__ == "__main__":
    unittest.main()
