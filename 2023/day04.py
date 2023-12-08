import functools
import re
from collections import defaultdict
from dataclasses import dataclass, field
from functools import cache
from typing import Any, Dict, List, Set, TypeVar


@dataclass(frozen=True)
class ScratchCard:
    winners: Set[int]
    numbers: List[int]


def parse_lines(lines: List[str]) -> List[ScratchCard]:
    ret = []
    for line in lines:
        the_rest = line.split(":")[1].strip()
        the_rest = re.sub(r"\s+", " ", the_rest)

        (left, right) = the_rest.split(" | ")
        winners = set([int(s.strip()) for s in left.split(" ")])
        numbers = [int(s.strip()) for s in right.split(" ")]
        ret.append(ScratchCard(winners=winners, numbers=numbers))
    return ret


def part_one(lines) -> int:
    cards = parse_lines(lines)

    total = 0
    for card in cards:
        match_count = sum(1 for x in card.numbers if x in card.winners)
        if match_count >= 1:
            total += 2 ** (match_count - 1)

    return total


def part_two(lines) -> int:
    cards = parse_lines(lines)

    multipliers = {x: 1 for x in range(len(cards))}

    for idx, card in enumerate(cards):
        match_count = sum(1 for x in card.numbers if x in card.winners)

        # the next m cards get a boost, multiplied by how many we already are at this rank
        for win in range(match_count):
            multipliers[idx + 1 + win] += multipliers[idx]

    # print(multipliers)
    return sum(multipliers.values())


def main() -> None:
    with open("day04_input.txt", "r") as file:
        lines = file.read().splitlines()
        print(part_one(lines))
        print(part_two(lines))


if __name__ == "__main__":
    main()
