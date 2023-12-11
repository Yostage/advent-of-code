import functools
import re
from dataclasses import dataclass, field
from functools import cache, cached_property
from itertools import groupby
from operator import methodcaller
from typing import Any, Dict, List, Tuple, TypeVar

FiveCardHand = Tuple[int, int, int, int, int]


@dataclass
class CamelCard:
    hand: FiveCardHand
    bid: int

    @cached_property
    def handrank(self) -> int:
        histogram = {k: len(list(g)) for k, g in groupby(sorted(self.hand))}
        frequencies = sorted(histogram.values())
        if frequencies == [5]:
            return 0
        if frequencies == [1, 4]:
            return -1
        if frequencies == [2, 3]:
            return -2
        if frequencies == [1, 1, 3]:
            return -3
        if frequencies == [1, 2, 2]:
            return -4
        if frequencies == [1, 1, 1, 2]:
            return -5
        assert frequencies == [1, 1, 1, 1, 1]
        return -6

    def sortkey(self) -> Tuple[int, int, int, int, int, int]:
        return (self.handrank, *self.hand)


def card_to_rank(c: str):
    values = {
        "A": 14,
        "K": 13,
        "Q": 12,
        "J": 11,
        "T": 10,
    }
    if c.isdigit():
        return int(c)
    return values[c]


def parse_lines(lines: List[str]) -> List[CamelCard]:
    cards: List[CamelCard] = []
    for line in lines:
        (hand, bid) = line.split(" ")
        cards.append(CamelCard(hand=list([card_to_rank(c) for c in hand]), bid=int(bid)))  # type: ignore
    return cards


def part_one(lines) -> int:
    cards = parse_lines(lines)
    return sum(
        [
            card.bid * (idx + 1)
            for idx, card in enumerate(sorted(cards, key=methodcaller("sortkey")))
        ]
    )
    # sum = 0
    # for idx, card in enumerate(sorted(cards, key=methodcaller("sortkey"))):
    #     sum += card.bid * (idx + 1)
    #     print(f"{card}: handrank {card.handrank}: rank {idx+1}")
    # return sum


def part_two(lines) -> int:
    parse_lines(lines)
    return 0


def main() -> None:
    with open("day07_input.txt", "r") as file:
        lines = file.read().splitlines()
        print(part_one(lines))
        print(part_two(lines))


if __name__ == "__main__":
    main()
