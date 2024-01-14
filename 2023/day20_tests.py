import unittest

from day20 import parse_lines, part_one, part_two


class TestDay20(unittest.TestCase):
    example = """broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a"""

    example2 = """broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output"""

    def test_parse_lines(self):
        parse_lines(self.example.splitlines())

    def test_part_one(self):
        result = part_one(self.example.splitlines())
        self.assertEqual(result, 32000000)
        result = part_one(self.example2.splitlines())
        self.assertEqual(result, 11687500)

    def test_part_two(self):
        result = part_two(self.example.splitlines())
        # self.assertEqual(result, xx)


if __name__ == "__main__":
    unittest.main()
