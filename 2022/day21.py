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
    up: Optional["Yell"] = field(init=False, repr=False, default=None)

    def as_python(self) -> str:
        if self.literal is not None:
            return f"{self.name} = {self.literal}"
        else:
            return f"{self.name} = {self.l} {self.op} {self.r}"


YellDict = Dict[str, Yell]


def hook_up_nodes(yells: YellDict, yell: Yell):
    # leaf nodes
    if yell.literal is not None:
        yell.left = None
        yell.right = None
        return

    # internal nodes
    yell.left = yells[yell.l]  # type: ignore
    assert yell.left is not yell
    yell.left.up = yell
    yell.right = yells[yell.r]  # type: ignore
    assert yell.right is not yell
    yell.right.up = yell
    hook_up_nodes(yells, yell.left)
    hook_up_nodes(yells, yell.right)


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

    hook_up_nodes(yells, yells["root"])
    return yells


def eval_from_root(yells: YellDict, root_node_name: str):
    for l in list(postorder_to_python(yells, yells[root_node_name])):
        # print(l)
        exec(l)
    return eval(root_node_name)


def part_one(lines) -> int:
    yells = parse_lines(lines)
    return eval_from_root(yells, "root")


def solve_for_x(yells: YellDict, node: Yell, x: str) -> None:
    # a = x + b -> x = a - b
    # a = x - b -> x = a + b
    # a = x * b -> x = a / b
    # a = x / b -> x = a * b

    # a = b + x -> x = a - b
    # a = b * x -> x = a / b
    # a = b - x -> x = b - a
    # a = b / x -> x = b / a

    inverses = {
        "+": "-",
        "-": "+",
        "*": "/",
        "/": "*",
    }
    assert node.op is not None
    a = node.name

    # rewrite ourselves to x
    node.name = x
    yells[node.name] = node

    if node.l == x:
        node.op = inverses[node.op]
        node.l = a
    else:
        if node.op in ["+", "*"]:
            node.op = inverses[node.op]
            node.r = node.l
            node.l = a
        else:
            node.r = a

    return


def part_two(lines) -> int:
    yells = parse_lines(lines)
    root = yells["root"]

    # start from humn
    # and propagate the solve upwards until we reach the root
    ptr = yells["humn"]
    floating_variable = ptr.name
    assert ptr is not None
    del yells["humn"]
    while ptr.up is not yells["root"]:
        assert ptr is not None
        parent = ptr.up
        assert parent is not None
        # print(f"Rewriting node {parent.as_python()} to solve for {floating_variable}")
        evicted_parent = parent.name
        solve_for_x(yells, parent, floating_variable)
        floating_variable = evicted_parent
        # print(f"Now it's [{parent.as_python()}]")
        ptr = parent

    # now we're at root.
    # before: root : left_side == right_side
    # now: floating_variable = the_other_side + 0
    root.name = floating_variable
    yells[root.name] = root
    if root.l == floating_variable:
        root.l = "zero"
    else:
        root.r = "zero"
    yells["zero"] = Yell(name="zero", literal=0, op=None, l=None, r=None)

    # rebuild the tree from humn which is the new root
    hook_up_nodes(yells, yells["humn"])
    # now we can solve for humn
    return eval_from_root(yells, "humn")


def postorder_to_python(yells: YellDict, yell: Yell) -> Generator[str, None, None]:
    # postorder traversal so we will get all the roots first
    if yell.left is not None:
        yield from postorder_to_python(yells, yell.left)
    if yell.right is not None:
        yield from postorder_to_python(yells, yell.right)
    yield yell.as_python()


def main() -> None:
    with open("day21_input.txt", "r") as file:
        lines = file.read().splitlines()
        print(part_one(lines))
        print(part_two(lines))


if __name__ == "__main__":
    main()
