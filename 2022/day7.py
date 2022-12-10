from functools import cache
import re
from typing import Any, Dict, List, Optional


from dataclasses import dataclass, field
from typing import TypeVar


@dataclass
class ElvenFile:
    name: str
    size: int


@dataclass
class ElvenDirectory:

    name: str
    parent: Optional["ElvenDirectory"]
    files: List[ElvenFile] = field(default_factory=list)
    directories: Dict[str, "ElvenDirectory"] = field(default_factory=dict)

    def __hash__(self) -> int:
        return self.get_full_name().__hash__()

    def get_full_name(self) -> str:
        tokens = []
        ptr = self
        while ptr:
            tokens.append(ptr.name)
            ptr = ptr.parent  # type: ignore
        return "/".join(reversed(tokens))

    @cache
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
            cwd = cwd.directories[filename]
        elif match := re.search(r"dir (\w+)", line):
            filename = str(match.groups()[0])
            assert cwd.directories.get(filename) is None
            cwd.directories[filename] = ElvenDirectory(name=filename, parent=cwd)
        elif line == "$ ls":
            continue
        elif line == "$ cd ..":
            cwd = cwd.parent  # type: ignore
        elif line == "$ cd /":
            cwd = root
        elif match := re.search(r"(\d+) ([\w\.])+", line):
            (size, name) = match.groups()
            cwd.files.append(ElvenFile(name=name, size=int(size)))
        else:
            print(f"UNMATCHED LINE {line}")
            assert False

    return root


def part_one(lines):
    root = parse_lines(lines)
    print(root.get_recursive_size())
    big_dirs = [d for d in root.dfs() if d.get_recursive_size() <= 100000]
    return sum([d.get_recursive_size() for d in big_dirs])


def part_two(lines):
    root = parse_lines(lines)
    total = 70000000
    need_available = 30000000
    current_available = total - root.get_recursive_size()
    need_to_find = need_available - current_available
    big_dirs = [d for d in root.dfs() if d.get_recursive_size() >= need_to_find]

    return min([d.get_recursive_size() for d in big_dirs])


def main():
    with open("day7_input.txt", "r") as file:
        lines = file.read().splitlines()
        print(part_two(lines))


if __name__ == "__main__":
    main()
