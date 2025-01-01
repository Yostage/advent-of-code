import functools
import re
from collections import deque
from dataclasses import dataclass, field
from functools import cache
from typing import Any, Deque, Dict, List, Set, Tuple, TypeVar


def parse_lines(lines: List[str]) -> Any:
    # each character is an alternating between a file length and a free block length
    # file x++ gets the following N slots
    # then the free list gets the next N slots
    files = {}
    freelist = deque()
    filecount = 0
    diskhead = 0
    disk = deque()

    for idx, c in enumerate(lines[0]):
        if idx % 2 == 0:
            # a new file with length n
            file_len = int(c)
            fileidx = filecount
            filecount += 1

            files[fileidx] = range(diskhead, diskhead + file_len)
            disk.extend([fileidx] * file_len)
            diskhead += file_len
        if idx % 2 == 1:
            # free spot
            free_len = int(c)
            freelist.extend(range(diskhead, diskhead + free_len))
            disk.extend([None] * free_len)
            diskhead += free_len

    return (files, freelist, disk)


def part_one(lines) -> int:
    (files, freelist, disk) = parse_lines(lines)
    # print(files)
    # print(freelist)
    # print(disk)
    for idx in reversed(range(len(disk))):
        # print(f"{idx}: {disk[idx]}")
        if len(freelist) == 0:
            break
        if disk[idx] is not None:
            if idx < freelist[0]:
                break
            freespot = freelist.popleft()
            disk[freespot] = disk[idx]
            disk[idx] = None
            freelist.append(idx)

    # parse the thing
    return sum(idx * val for idx, val in enumerate(disk) if val is not None)


def part_two(lines) -> int:
    parse_lines(lines)
    return 0


def main() -> None:
    with open("day09_input.txt", "r") as file:
        lines = file.read().splitlines()
        print(part_one(lines))
        print(part_two(lines))


if __name__ == "__main__":
    main()
