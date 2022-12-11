import functools
import re
from dataclasses import dataclass, field
from functools import cache
from typing import Any, Dict, List, TypeVar


@dataclass
class Monkey:
    operation: str = ""
    items: List[int] = field(default_factory=list)
    test_divisor: int = 0
    monkey_targets: List[int] = field(default_factory=list)
    count_inspected_items: int = 0


def parse_lines(lines: List[str]) -> List[Monkey]:
    monkeys = []
    new_monkey = Monkey()

    for line in lines:
        line = line.strip()
        if line == "":
            continue
        elif line.startswith("Monkey"):
            new_monkey = Monkey()
            monkeys.append(new_monkey)

        elif match := re.search("Starting items: (.*)", line):
            new_monkey.items = [int(n) for n in str(match.groups()[0]).split(", ")]
        elif match := re.search("Operation: new = (.*)", line):
            new_monkey.operation = str(match.groups()[0])
        elif match := re.search("Test: divisible by (\d+)", line):
            new_monkey.test_divisor = int(match.groups()[0])
        elif match := re.search("If true: throw to monkey (\d+)", line):
            new_monkey.monkey_targets = [0] * 2
            new_monkey.monkey_targets[0] = int(match.groups()[0])
        elif match := re.search("If false: throw to monkey (\d+)", line):
            new_monkey.monkey_targets[1] = int(match.groups()[0])
        else:
            raise RuntimeError(f"couldn't parse [{line}]")

    return monkeys


def take_turn(monkeys: List[Monkey], monkey_index: int) -> None:
    def mutate_item(item: int, operation: str) -> int:
        old = item
        return eval(operation)

    m = monkeys[monkey_index]
    while len(m.items) > 0:
        item = m.items.pop(0)

        # while monkey has items
        # pop first item
        # inspect it: mutate with the operator
        item = mutate_item(item, m.operation)
        # apply boredom
        item = item // 3

        # increment inspection count
        m.count_inspected_items += 1
        # test it: check the divisor
        # toss it: enqueue
        dest = (
            m.monkey_targets[0] if item % m.test_divisor == 0 else m.monkey_targets[1]
        )
        # print(f"item {item} to monkey {m.monkey_targets[0]}")

        monkeys[dest].items.append(item)


def take_round(monkeys: List[Monkey]) -> None:
    for idx, _ in enumerate(monkeys):
        take_turn(monkeys, idx)
    print("After round report:")
    for idx, m in enumerate(monkeys):
        print(f"Monkey {idx}: {m.items}")


def part_one(lines):
    monkeys = parse_lines(lines)
    for round in range(20):
        take_round(monkeys)
    inspected = [m.count_inspected_items for m in monkeys]
    print(f"Monkey inspection count: {inspected}")
    inspected.sort()
    return inspected[-1] * inspected[-2]


def part_two(lines):
    parse_lines(lines)
    return None


def main():
    with open("day11_input.txt", "r") as file:
        lines = file.read().splitlines()
        print(part_one(lines))
        print(part_two(lines))


if __name__ == "__main__":
    main()
