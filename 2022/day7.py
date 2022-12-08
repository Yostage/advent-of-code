import re
from typing import List


def parse_lines(lines: List[str]):
    for line in lines:
        if match := re.search(r"\$ cd (\w+)", line):
            (filename) = match.groups()
            print(f"CD into {filename}")
        elif match := re.search(r"dir (\w+)", line):
            (filename) = match.groups()
            print(f"child dir {filename}")
        elif line == "$ ls":
            print("ls")
        elif line == "$ cd ..":
            print("cd up")
        elif line == "$ cd /":
            print("cd root")
        elif match := re.search(r"(\d+) ([\w\.])+", line):
            (size, name) = match.groups()
            print(f"file [{name}] has size [{size}]")
        else:
            print(f"UNMATCHED LINE {line}")
        # else:
        # print(f"Not match [{line}]")

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
