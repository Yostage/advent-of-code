import functools
import re
from dataclasses import dataclass, field
from functools import cache
from typing import Any, Deque, Dict, List, Set, Tuple, TypeVar

part_spec = List[str]
workflow = List[str]
# workflow_dict = Dict[str, workflow]


def parse_lines(lines: List[str]) -> Tuple[Dict[str, workflow], List[part_spec]]:
    workflows = {}
    line_iter = iter(lines)
    for line in line_iter:
        if line == "":
            break
        (prefix, rest) = line.split("{")
        workflows[prefix] = rest[:-1].split(",")

    parts = [line[1:-1].split(",") for line in line_iter]

    # qqz{s>2770:qs,m<1801:hdj,R}
    return (workflows, parts)


# @cache
def workflow_to_evaluator(w: workflow) -> str:
    # s>2770:qs,m<1801:hdj,R
    evaluators: List[str] = []
    for step in w:
        if ":" in step:
            (predicate, result) = step.split(":")
            evaluators.append(f"'{result}' if {predicate} else")
        else:
            evaluators.append(f"'{step}'")
    return " ".join(evaluators)


def score_part(part: part_spec, workflow_dict: Dict[str, workflow]) -> int:
    # x = m = a = s = 0
    # load up all the variables
    for stat in part:
        # print(stat)
        exec(stat)

    next_state = "in"
    while next_state not in ["A", "R"]:
        workflow = workflow_dict[next_state]
        next_state = eval(workflow_to_evaluator(workflow))

    if next_state == "A":
        return eval("x + m + a + s")
    else:
        assert next_state == "R"
        return 0


def part_one(lines: List[str]) -> int:
    (workflows, parts) = parse_lines(lines)
    print(workflows)
    # for w in workflows.values():
    #     print(workflow_to_evaluator(tuple(w)))
    # print(parts)
    return sum(score_part(part, workflows) for part in parts)


def part_two(lines) -> int:
    parse_lines(lines)
    return 0


def main() -> None:
    with open("day19_input.txt", "r") as file:
        lines = file.read().splitlines()
        print(part_one(lines))
        print(part_two(lines))


if __name__ == "__main__":
    main()
