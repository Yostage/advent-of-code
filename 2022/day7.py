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


def parse_lines(lines: List[str]):
    root = ElvenDirectory(name="/", parent=None)
    cwd = root
    for line in lines:
        if match := re.search(r"\$ cd (\w+)", line):
            (filename) = match.groups()
            print(f"CD into {filename}")
            cwd = cwd.directories[str(filename)]
        elif match := re.search(r"dir (\w+)", line):
            (filename) = match.groups()
            print(f"child dir {filename}")
            cwd.directories[str(filename)] = ElvenDirectory(
                name=str(filename), parent=cwd
            )
        elif line == "$ ls":
            print("ls")
        elif line == "$ cd ..":
            print("cd up")
            cwd = cwd.parent
        elif line == "$ cd /":
            print("cd root")
            cwd = root
        elif match := re.search(r"(\d+) ([\w\.])+", line):
            (size, name) = match.groups()
            print(f"file [{name}] has size [{size}]")
            cwd.files.append(ElvenFile(name=name, size=int(size)))
        else:
            print(f"UNMATCHED LINE {line}")
            assert False

    return None


def main():
    with open("day7_input.txt", "r") as file:
        lines = file.read().splitlines()
        parse_lines(lines)

    # part one
    # print(find_signal(lines[0]))
    # part two
    # print(find_signal(lines[0], 14))


if __name__ == "__main__":
    main()
