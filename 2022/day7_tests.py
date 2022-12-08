import functools
import itertools
import unittest
from typing import Iterator

from day7 import parse_lines, part_one, part_two


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
        # part_one(self.example1.splitlines())
        # root = parse_lines(self.example1.splitlines())

        # print(root.get_recursive_size())
        # # self.assertEqual(find_signal(self.example1), 5)

        # big_dirs = [d for d in root.dfs() if d.get_recursive_size() < 100000]
        # print(sum([d.get_recursive_size() for d in big_dirs]))
        # for d in root.dfs():
        # print(f"Traversing directory {d.name}")

        self.assertEqual(part_one(self.example1.splitlines()), 95437)

    def test_part_two(self):
        self.assertEqual(part_two(self.example1.splitlines()), 24933642)
        # self.assertTrue(True)


if __name__ == "__main__":
    unittest.main()
