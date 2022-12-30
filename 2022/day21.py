import functools
import re
from dataclasses import dataclass, field
from functools import cache
from typing import Any, Dict, Generator, List, Optional, TypeVar


@dataclass
class Yell:
    name: str
    literal: Optional[int]
    l: Optional[str]
    r: Optional[str]
    op: Optional[str]
    left: Optional["Yell"] = field(init=False, repr=False, default=None)
    right: Optional["Yell"] = field(init=False, repr=False, default=None)

    def as_python(self) -> str:
        if self.literal is not None:
            return f"{self.name} = {self.literal}"
        else:
            return f"{self.name} = {self.l} {self.op} {self.r}"


YellDict = Dict[str, Yell]


def parse_lines(lines: List[str]) -> Dict[str, Yell]:
    yells: Dict[str, Yell] = {}
    # dbpl: 5
    # cczh: sllz + lgvd
    binary = r"(\w{4}): (\w{4}) (.) (\w{4})"
    literal = r"(\w{4}): (\d+)"
    for line in lines:
        if match := re.search(binary, line):
            yells[match[1]] = Yell(
                name=match[1], literal=None, l=match[2], op=match[3], r=match[4]
            )
        elif match := re.search(literal, line):
            yells[match[1]] = Yell(
                name=match[1],
                literal=int(match[2]),
                l=None,
                op=None,
                r=None,
            )
        else:
            raise AssertionError(f"couldn't parse [{line}]")

    # hook up all the edges
    for yell in yells.values():
        if yell.literal is None:
            # print(f"Yell {yell.name} had children")
            yell.left = yells[yell.l]  # type: ignore
            yell.right = yells[yell.r]  # type: ignore
            # print(f"Hooked up l={yell.left} and r={yell.right}")

    return yells


def part_one(lines) -> int:
    yells = parse_lines(lines)
    for l in list(top_down_execution(yells, yells["root"])):
        # print(l)
        exec(l)
    return eval("root")
    # return 0


def top_down_execution(yells: YellDict, yell: Yell) -> Generator[str, None, None]:
    # traverse the tree in preorder
    # print it out in reverse
    print(f"Visiting {yell.name}")
    if yell.left is not None:
        yield from top_down_execution(yells, yell.left)
    if yell.right is not None:
        yield from top_down_execution(yells, yell.right)
    yield yell.as_python()


def part_two(lines) -> int:
    parse_lines(lines)
    return 0


def main() -> None:
    with open("day21_input.txt", "r") as file:
        lines = file.read().splitlines()
        print(part_one(lines))
        print(part_two(lines))


if __name__ == "__main__":
    main()
