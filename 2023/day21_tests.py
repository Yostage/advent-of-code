import unittest

from day21 import parse_lines, part_one, part_two

# January 7 11:18 PM Drilian: 21 probably worst of the remainders
# January 7 11:14 PM Drilian: For 21 I will say
# January 7 11:14 PM Drilian: well, for part 2
# January 7 11:15 PM Drilian: you're gonna get the usual big fucking number of things to do
# January 7 11:15 PM Drilian: look at how it is modulo the size of the grid
# January 7 11:15 PM Drilian: and maybe graph what it looks like when you go THAT far
# January 7 11:15 PM Drilian: and notice what is going on
# January 7 11:15 PM Drilian: and it will save you a ton of time

# January 7 11:16 PM Drilian: 22 was fun
# January 7 11:16 PM Drilian: 23 was tricky but manageably tricky
# January 7 11:17 PM Drilian: 24 is the one where I was bitter that I did just an absolute shitload of math and a bunch of people just threw it into a python solver library
# January 7 11:17 PM Drilian: and 25 took me a while to figure out what the fuck even to do but it only has a part 1 because it's 25
# January 7 11:18 PM Drilian: and I will happily give you time-saving hints if you want them


class TestDay21(unittest.TestCase):
    example = """...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
..........."""

    def test_parse_lines(self):
        parse_lines(self.example.splitlines())

    def test_part_one(self):
        result = part_one(self.example.splitlines())
        self.assertEqual(result, 16)

    def test_part_two(self):
        result = part_two(self.example.splitlines())
        # self.assertEqual(result, xx)


if __name__ == "__main__":
    unittest.main()
