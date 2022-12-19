from functools import cmp_to_key
from math import copysign
from typing import Any, List

from more_itertools import batched, flatten


def sign(x: int) -> int:
    return 0 if x == 0 else int(copysign(1, x))


def compare(left: List | int, right: List | int) -> int:
    if isinstance(left, int) and isinstance(right, int):
        return sign(left - right)
    elif isinstance(left, List) and isinstance(right, List):
        for pair in zip(left, right):
            pairwise = compare(pair[0], pair[1])
            # print(f"Zipped {pair} = {pairwise}")
            if pairwise != 0:
                return pairwise

        # left list should be shorter
        # every entry in list should be
        return compare(len(left), len(right))
    else:
        if isinstance(left, int):
            return compare([left], right)
        else:
            return compare(left, [right])


def parse_lines(lines: List[str]) -> Any:
    return [
        (eval(pair[0]), eval(pair[1]))
        for pair in batched(filter(lambda l: len(l) > 0, lines), 2)
    ]


def part_one(lines) -> int:
    pairs = parse_lines(lines)
    results = [compare(left, right) for left, right in pairs]
    total = 0
    print(results)
    for idx, result in enumerate(results):
        if result != 1:
            total += idx + 1
    return total


def part_two(lines) -> int:
    pairs = parse_lines(lines)
    all = list(flatten(pairs))
    decoder1 = [[2]]
    decoder2 = [[6]]
    all += [decoder1, decoder2]
    all.sort(key=cmp_to_key(compare))
    return (all.index(decoder1) + 1) * (all.index(decoder2) + 1)


def main() -> None:
    with open("day13_input.txt", "r") as file:
        lines = file.read().splitlines()
        print(part_one(lines))
        print(part_two(lines))


if __name__ == "__main__":
    main()
