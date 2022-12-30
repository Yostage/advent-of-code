import functools
import re
from dataclasses import dataclass, field
from functools import cache
from operator import attrgetter
from typing import Any, Dict, List, TypeVar

from day13 import sign


@dataclass
class MixableNumber:
    val: int
    pos: int


def parse_lines(lines: List[str]) -> List[MixableNumber]:
    return [MixableNumber(int(line), idx) for idx, line in enumerate(lines)]


def mix(mx: MixableNumber, numbers: List[MixableNumber]) -> None:
    ring = len(numbers)
    old_loc = mx.pos
    # ring - 1 because the being last and being first are the same. there's
    # one fewer slot than you think there are
    new_loc = (mx.val + mx.pos) % (ring - 1)

    if old_loc == new_loc:
        return

    # print(f"{mx.val} moves from {old_loc} to {new_loc}")
    mx.pos = new_loc
    for num in numbers:
        # we already processed this
        if num is mx:
            continue

        # we always need to visit new, because somebody is still there.
        # we don't need to visit old because we evacuated it

        # we moved backwards, everybody shift up
        if new_loc < old_loc:
            if new_loc <= num.pos and num.pos < old_loc:
                num.pos += 1
        # everybody shift back
        if old_loc < new_loc:
            if old_loc < num.pos and num.pos <= new_loc:
                num.pos -= 1


def val_at_pos(pos: int, numbers: List[MixableNumber]) -> int:
    ring = len(numbers)
    pos = pos % ring
    for mx in numbers:
        if mx.pos == pos:
            return mx.val
    assert False


def verify_integrity(numbers: List[MixableNumber]) -> None:
    positions: Dict[int, MixableNumber] = dict()
    for mx in numbers:
        if mx.pos in positions:
            raise AssertionError(f"{mx} and {positions[mx.pos]} collision")
        positions[mx.pos] = mx

    ring = len(numbers)
    assert len(positions) == ring
    assert min(positions.keys()) == 0
    assert max(positions.keys()) == ring - 1


def find_val(val: int, numbers: List[MixableNumber]) -> int:
    for mx in numbers:
        if mx.val == val:
            return mx.pos
    assert False


def printable_vals(numbers: List[MixableNumber]) -> str:
    s = sorted(numbers, key=attrgetter("pos"))
    return ", ".join(str(mx.val) for mx in s)


def part_one(lines) -> int:

    # mix every number
    # 1000th, 2000th, and 3000th numbers after the value 0
    nums = parse_lines(lines)

    # print(printable_vals(nums))
    # print("Mixing")
    for num in nums:
        mix(num, nums)
        verify_integrity(nums)
        # print(printable_vals(nums))

    zero_pos = find_val(0, nums)
    print(f"The zero was at pos {zero_pos}")
    for offset in [1000, 2000, 3000]:
        print(
            f"Value at {offset+zero_pos}({(offset+zero_pos)% len(nums)}) is {val_at_pos(offset+zero_pos,nums)}"
        )
    return sum((val_at_pos(offset + zero_pos, nums) for offset in [1000, 2000, 3000]))


def part_two(lines) -> int:
    parse_lines(lines)
    return 0


def main() -> None:
    with open("day20_input.txt", "r") as file:
        lines = file.read().splitlines()
        print(part_one(lines))
        # print(part_two(lines))


if __name__ == "__main__":
    main()
