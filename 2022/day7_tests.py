import functools
import itertools
import unittest
from typing import Iterator

from day7 import parse_lines


class TestDay7(unittest.TestCase):

    example1 = """$ cd /
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
        parse_lines(self.example1.splitlines())
        # self.assertEqual(find_signal(self.example1), 5)
        self.assertTrue(True)


if __name__ == "__main__":
    unittest.main()
