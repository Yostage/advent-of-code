from functools import cache
import re
from typing import Any, Dict, List


from dataclasses import dataclass, field
from typing import TypeVar

# SelfElvenDirectory = TypeVar("SelfElvenDirectory", bound="ElvenDirectory")


@dataclass
class ElvenFile:
    name: str
    size: int


@dataclass
class ElvenDirectory:
    # SelfElvenDirectory = TypeVar("SelfElvenDirectory", bound="ElvenDirectory")

    name: str
    parent: Any
    files: List[ElvenFile] = field(default_factory=list)
    directories: Dict[str, Any] = field(default_factory=dict)

    # @cache
    def get_recursive_size(self) -> int:
        return sum([f.size for f in self.files]) + sum(
            [d.get_recursive_size() for d in self.directories.values()]
        )

    def dfs(self):
        for d in self.directories.values():
            yield from d.dfs()
        yield self


def parse_lines(lines: List[str]) -> ElvenDirectory:
    root = ElvenDirectory(name="/", parent=None)
    cwd = root

    for line in lines:
        if match := re.search(r"\$ cd (\w+)", line):
            filename = str(match.groups()[0])
            # print(f"CD into {filename}")
            cwd = cwd.directories[filename]
        elif match := re.search(r"dir (\w+)", line):
            filename = str(match.groups()[0])
            # print(f"child dir {filename}")
            assert cwd.directories.get(filename) is None
            cwd.directories[filename] = ElvenDirectory(name=filename, parent=cwd)
            # print(f"\tcwd {cwd.name} now has {len(cwd.directories.values())} children")
        elif line == "$ ls":
            # print("ls")
            continue
        elif line == "$ cd ..":

            cwd = cwd.parent
            # print(f"cd .. [cwd is now {cwd.name}]")
        elif line == "$ cd /":
            # print("cd root")
            cwd = root
        elif match := re.search(r"(\d+) ([\w\.])+", line):
            (size, name) = match.groups()
            # print(f"file [{name}] has size [{size}]")
            cwd.files.append(ElvenFile(name=name, size=int(size)))
        else:
            print(f"UNMATCHED LINE {line}")
            assert False

    return root


def part_one(lines):
    root = parse_lines(lines)
    print(root.get_recursive_size())
    # self.assertEqual(find_signal(self.example1), 5)

    # for d in root.dfs():
    #     print(f"directory {d.name} has size {d.get_recursive_size()}")
    big_dirs = [d for d in root.dfs() if d.get_recursive_size() <= 100000]
    return sum([d.get_recursive_size() for d in big_dirs])
    # print(sum([d.get_recursive_size() for d in big_dirs]))


def part_two(lines):
    root = parse_lines(lines)
    total = 70000000
    need_available = 30000000
    current_available = total - root.get_recursive_size()
    need_to_find = need_available - current_available
    # print(root.get_recursive_size())
    # self.assertEqual(find_signal(self.example1), 5)

    # for d in root.dfs():
    #     print(f"directory {d.name} has size {d.get_recursive_size()}")
    big_dirs = [d for d in root.dfs() if d.get_recursive_size() >= need_to_find]

    # for d in big_dirs:
    #     print(f"{d.name}: {d.get_recursive_size()}")
    return min([d.get_recursive_size() for d in big_dirs])
    # print(sum([d.get_recursive_size() for d in big_dirs]))


def main():
    with open("day7_input.txt", "r") as file:
        lines = file.read().splitlines()
        print(part_two(lines))

    # part one
    # print(find_signal(lines[0]))
    # part two
    # print(find_signal(lines[0], 14))


if __name__ == "__main__":
    main()
