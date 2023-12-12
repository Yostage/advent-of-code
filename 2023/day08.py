import functools
import math
import re
from collections import defaultdict
from dataclasses import dataclass, field
from functools import cache
from itertools import cycle
from typing import Any, Dict, List, Set, TypeVar


def parse_lines(lines: List[str]) -> Any:
    instructions = [c for c in lines[0]]
    lefts: Dict[str, str] = {}
    rights: Dict[str, str] = {}
    for line in lines[2:]:
        node, rest = line.split(" = ")
        (left, right) = rest[1:-1].split(", ")
        lefts[node] = left
        rights[node] = right

    return (instructions, {"L": lefts, "R": rights})


def part_one(lines) -> int:
    (instructions, nested_map) = parse_lines(lines)
    current_node = "AAA"
    for idx, step in enumerate(cycle(instructions)):
        current_node = nested_map[step][current_node]
        if current_node == "ZZZ":
            return idx + 1
    assert False


def part_two(lines) -> int:
    (instructions, nested_map) = parse_lines(lines)
    starting_nodes = {n for n in nested_map["L"].keys() if n[2] == "A"}
    terminal_nodes = {n for n in nested_map["L"].keys() if n[2] == "Z"}
    print(f"Starting nodes = {starting_nodes}")
    print(f"Terminal nodes = {terminal_nodes}")

    def get_all_wins(starting_node):
        # count total steps + location. Find all of them until we hit a repeat
        terminal_states = list()
        # index into the instructions + location. This is our full state and if it
        # ever repeats then we have fully consumed the generator
        visited = set()
        current_node = starting_node
        for total_steps, (step_index, step) in enumerate(
            cycle(enumerate(instructions))
        ):
            # take a step
            current_node = nested_map[step][current_node]
            if current_node in terminal_nodes:
                terminal_states.append(total_steps + 1)
                # record that at time t we were at winning node n
                # if we ever see a dupe, we've hit a cycle
            current_global_state = (step_index, current_node)
            if current_global_state in visited:
                return terminal_states
            else:
                visited.add(current_global_state)

    all_wins = {
        starting_node: get_all_wins(starting_node) for starting_node in starting_nodes
    }

    # when will the stars align?
    # determined by inspection that there's only one solution in each graph, so we can just use the first one
    return math.lcm(*[wins[0] for wins in all_wins.values()])


def main() -> None:
    with open("day08_input.txt", "r") as file:
        lines = file.read().splitlines()
        print(part_one(lines))
        print(part_two(lines))


if __name__ == "__main__":
    main()
