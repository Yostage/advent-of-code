import functools
import re
from dataclasses import dataclass, field
from functools import cache
from typing import Any, Deque, Dict, List, Set, Tuple, TypeVar


def parse_lines(lines: List[str]) -> Any:
    rules = []
    updates = []
    line_iter = iter(lines)
    for line in line_iter:

        if line == "":
            break
        rules.append(line.split("|"))
    for line in line_iter:
        updates.append(line.split(","))

    return (rules, updates)


def test_update(rules, update):
    page_order_map = {page: index for index, page in enumerate(update)}
    print(page_order_map)
    for rule in rules:
        if (
            rule[0] in page_order_map
            and rule[1] in page_order_map
            and page_order_map[rule[0]] > page_order_map[rule[1]]
        ):
            print(f"Rule {rule} violated for {update}")
            return 0

    return int(update[len(update) // 2])


def part_one(lines) -> int:
    (rules, updates) = parse_lines(lines)
    print(rules)
    print
    print(updates)

    return sum(test_update(rules, update) for update in updates)


def part_two(lines) -> int:
    parse_lines(lines)
    return 0


def main() -> None:
    with open("day05_input.txt", "r") as file:
        lines = file.read().splitlines()
        print(part_one(lines))
        print(part_two(lines))


if __name__ == "__main__":
    main()
