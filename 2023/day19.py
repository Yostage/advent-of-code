import math
from typing import Dict, List, Mapping, Tuple

from util import Point2D

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


ScoreDict = Dict[str, Point2D]

ScoreTuple = Tuple[
    Tuple[str, Point2D], Tuple[str, Point2D], Tuple[str, Point2D], Tuple[str, Point2D]
]


def score(s: ScoreDict):
    return math.prod(1 + v[1] - v[0] for v in s.values())


def split_interval(input: Point2D, test: str, target: int) -> Tuple[Point2D, Point2D]:
    # [0,100] vs. x < 50:
    # [0,49] . [50,100]
    if test == "<":
        true_side = (input[0], target - 1)
        false_side = (target, input[1])
    elif test == ">":
        false_side = (input[0], target)
        true_side = (target + 1, input[1])
    else:
        raise ValueError(test)

    return (true_side, false_side)


def score_dict_to_state(d: ScoreDict) -> ScoreTuple:
    return tuple(sorted(d.items()))  # type:ignore


def calculate_all_score(
    score_state: ScoreTuple, workflow_dict: Dict[str, workflow], workflow_key
) -> int:
    sum = 0

    # base case:
    if workflow_key == "A":
        return score(dict(score_state))
    elif workflow_key == "R":
        return 0

    current_score = dict(score_state)

    # recursive case
    this_workflow = workflow_dict[workflow_key]
    for step in this_workflow:
        if ":" in step:
            (predicate, result) = step.split(":")
            (var, test, target) = (predicate[0], predicate[1], predicate[2:])
            interval = current_score[var]
            (true_side, false_side) = split_interval(interval, test, int(target))
            # clone current score
            recursive_score = current_score.copy()
            # mutate it to pass the predicate, and sum up the recursion case for the target
            recursive_score[var] = true_side
            sum += calculate_all_score(
                score_dict_to_state(recursive_score), workflow_dict, workflow_key=result
            )

            # then mutate the current score and keep going
            current_score[var] = false_side
            # evaluators.append(f"'{result}' if {predicate} else")

        else:
            # no predicate, constant node
            sum += calculate_all_score(
                score_dict_to_state(current_score), workflow_dict, workflow_key=step
            )

    # we'll do this multiple times
    score_dict = dict(score_state)
    return sum


def part_two(lines) -> int:
    parse_lines(lines)
    (workflows, _) = parse_lines(lines)
    initial_state = {rating: (1, 4000) for rating in ("x", "m", "a", "s")}
    return calculate_all_score(score_dict_to_state(initial_state), workflows, "in")  # type: ignore


def main() -> None:
    with open("day19_input.txt", "r") as file:
        lines = file.read().splitlines()
        print(part_one(lines))
        print(part_two(lines))


if __name__ == "__main__":
    main()
