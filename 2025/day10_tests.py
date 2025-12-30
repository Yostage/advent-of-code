import unittest

from day10 import parse_lines, part_one, part_two


class TestDay10(unittest.TestCase):
    example = """[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}"""

    rong = """[##.##.###] (0,1,4,5,6,7,8) (1,2,3,4,5,6,8) (1,4,6) (1,5,6) (0,2,4,5,7) (0,1,3,4,6,7,8) (0,2,6,8) (2,3,6,7) (0,2,3,4,6,7) (2,5) (0,1,3,4,5,6,7,8) {87,72,71,70,99,64,112,89,62}"""

    def test_parse_lines(self):
        parse_lines(self.example.splitlines())

    def test_part_one(self):
        result = part_one(self.example.splitlines())
        self.assertEqual(result, 7)

    def test_part_two(self):
        result = part_two(self.example.splitlines())
        self.assertEqual(result, 33)

    def test_part_two_rong(self):
        result = part_two(self.rong.splitlines())
        self.assertEqual(result, 128)


if __name__ == "__main__":
    unittest.main()
