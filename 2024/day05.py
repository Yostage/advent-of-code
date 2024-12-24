from collections import deque
from typing import Any, List


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
    # print(page_order_map)
    print(f"Testing : {update}")
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
    return sum(test_update(rules, update) for update in updates)


def sort_update(rules, update):
    updates_remaining = set(update)
    sorted = deque([])
    relevant_rules = rules
    while len(updates_remaining) > 0:
        print(f"Sorting {updates_remaining}")

        # base case
        if len(updates_remaining) == 1:
            sorted.appendleft(updates_remaining.pop())
            return sorted

        relevant_rules = [
            rule
            for rule in relevant_rules
            if rule[0] in updates_remaining and rule[1] in updates_remaining
        ]
        print(relevant_rules)

        # which element is never first
        firsts = set(rule[0] for rule in relevant_rules)
        left_out = updates_remaining - firsts
        assert len(left_out) == 1
        last = left_out.pop()
        sorted.appendleft(last)
        updates_remaining.remove(last)
    assert False


def part_two(lines) -> int:
    parse_lines(lines)
    (rules, updates) = parse_lines(lines)

    broken_updates = filter(lambda update: test_update(rules, update) == 0, updates)
    sorted_broken_updates = [sort_update(rules, update) for update in broken_updates]
    return sum(test_update(rules, update) for update in sorted_broken_updates)


def main() -> None:
    with open("day05_input.txt", "r") as file:
        lines = file.read().splitlines()
        print(part_one(lines))
        print(part_two(lines))


if __name__ == "__main__":
    main()
