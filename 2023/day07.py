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
        frequencies = tuple(sorted(histogram.values()))

        joker_histogram = {
            k: len(list(g))
            for k, g in groupby(sorted([c for c in self.hand if c != 1]))
        }
        joker_frequencies = list(sorted(joker_histogram.values()))
        if len(joker_frequencies) > 0:
            joker_frequencies[-1] += sum(1 for c in self.hand if c == 1)

        hand_ranks = {
            (5,): 0,
            (1, 4): -1,
            (2, 3): -2,
            (1, 1, 3): -3,
            (1, 2, 2): -4,
            (1, 1, 1, 2): -5,
            (1, 1, 1, 1, 1): -6,
            tuple(): -7,
        }
        return max(hand_ranks[frequencies], hand_ranks[tuple(joker_frequencies)])

    def sortkey(self) -> Tuple[int, int, int, int, int, int]:
        return (self.handrank, *self.hand)


def card_to_rank(c: str):
    values = {
        "A": 14,
        "K": 13,
        "Q": 12,
        "J": 11,
        "*": 1,
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
    sum = 0
    for idx, card in enumerate(sorted(cards, key=methodcaller("sortkey"))):
        sum += card.bid * (idx + 1)
        # print(f"{card}: handrank {card.handrank}: rank {idx+1}")
    return sum


def part_two(lines) -> int:
    cards = parse_lines([line.replace("J", "*") for line in lines])
    sum = 0
    for idx, card in enumerate(sorted(cards, key=methodcaller("sortkey"))):
        sum += card.bid * (idx + 1)
        # print(f"{card}: handrank {card.handrank}: rank {idx+1}")
    return sum


def main() -> None:
    with open("day07_input.txt", "r") as file:
        lines = file.read().splitlines()
        print(part_one(lines))
        print(part_two(lines))


if __name__ == "__main__":
    main()
