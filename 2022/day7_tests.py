import functools
import itertools
import unittest
from typing import Iterator

from day7 import parse_lines, part_one, part_two


class TestDay7(unittest.TestCase):

    example = """$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k"""

    def test_part_one(self):
        self.assertEqual(part_one(self.example.splitlines()), 95437)

    def test_part_two(self):
        self.assertEqual(part_two(self.example.splitlines()), 24933642)


if __name__ == "__main__":
    unittest.main()
