import functools
import re
from collections import OrderedDict, deque
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

            files[fileidx] = (diskhead, file_len)
            disk.extend([fileidx] * file_len)
            diskhead += file_len
        if idx % 2 == 1:
            # free spot
            free_len = int(c)
            freelist.extend(range(diskhead, diskhead + free_len))
            disk.extend([None] * free_len)
            diskhead += free_len

    return (files, freelist, disk)


def parse_lines2(lines: List[str]) -> Any:
    # each character is an alternating between a file length and a free block length
    # file x++ gets the following N slots
    # then the free list gets the next N slots
    files = OrderedDict()
    freelist = deque()
    filecount = 0
    diskhead = 0

    for idx, c in enumerate(lines[0]):
        if idx % 2 == 0:
            # a new file with length n
            l = int(c)
            files[filecount] = (diskhead, l)
            filecount += 1
            diskhead += l
        if idx % 2 == 1:
            # free spot
            l = int(c)
            freelist.append((diskhead, l))
            diskhead += l

    return (files, freelist)


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
    (files, freelist) = parse_lines2(lines)
    # print(files)
    # print(freelist)
    # print(disk)

    for filenum, v in reversed(files.items()):
        (file_start, file_len) = v

        if len(freelist) == 0:
            break
        # attempt to move this file into each freelist spot, starting with the first, break it up if necessary
        for free_start, free_len in sorted(freelist):

            if free_len < file_len:
                continue
            if file_start < free_start:
                continue

            # print("Moving file", filenum, "to", free_start, "from", file_start)
            freelist.remove((free_start, free_len))
            files[filenum] = (free_start, file_len)
            if free_len > file_len:
                freelist.appendleft((free_start + file_len, free_len - file_len))
            break
    # nx + (n(n-1))/2
    sum = 0
    for idx, (start, l) in files.items():
        sum += idx * (start * l + (l * (l - 1)) // 2)
    return sum


def main() -> None:
    with open("day09_input.txt", "r") as file:
        lines = file.read().splitlines()
        print(part_one(lines))
        print(part_two(lines))


if __name__ == "__main__":
    main()
