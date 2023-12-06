import functools
import math
import re
from dataclasses import dataclass, field
from functools import cache
from typing import Any, Dict, List, TypeVar

from util import Point2D, tuple2_add


@dataclass(frozen=True)
class SchematicNumber:
    number: int
    lhs: Point2D


def get_adjacency_list() -> List[Point2D]:
    adjacencies = [(x, y) for x in [-1, 0, 1] for y in [-1, 0, 1]]
    adjacencies.remove((0, 0))
    return adjacencies


@dataclass
class Schematic:
    symbols: Dict[Point2D, str]
    numbers: Dict[Point2D, SchematicNumber]

    def get_expanded_number_map(self):
        return {
            (number.lhs[0] + dx, number.lhs[1]): number
            for number in self.numbers.values()
            for dx in range(0, len(str(number.number)))
        }


def parse_lines(lines: List[str]) -> Any:
    symbols: Dict[Point2D, str] = {}
    numbers: Dict[Point2D, SchematicNumber] = {}
    number_lhs: Point2D = (-1, -1)
    number_accumulator = ""

    def close_accumulator() -> None:
        nonlocal number_accumulator
        nonlocal numbers
        if number_accumulator == "":
            return
        s = SchematicNumber(int(number_accumulator), number_lhs)
        numbers[s.lhs] = s
        number_accumulator = ""

    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            if c.isdigit():
                if number_accumulator == "":
                    number_lhs = (x, y)

                number_accumulator += c
                continue
            else:
                close_accumulator()

            if c == ".":
                continue

            # symbol
            symbols[(x, y)] = c
        close_accumulator()

    return Schematic(symbols=symbols, numbers=numbers)


def part_one(lines) -> int:
    expanded_number_map: Dict[Point2D, SchematicNumber] = {}

    schematic = parse_lines(lines)

    expanded_number_map = schematic.get_expanded_number_map()

    # find every number adjacent to a symbol
    part_numbers = set()
    for symbol_loc in schematic.symbols:
        for adj in get_adjacency_list():
            target = tuple2_add(symbol_loc, adj)
            if target in expanded_number_map:
                part_numbers.add(expanded_number_map[target])

    return sum([p.number for p in part_numbers])


def part_two(lines) -> int:
    expanded_number_map: Dict[Point2D, SchematicNumber] = {}

    schematic = parse_lines(lines)

    expanded_number_map = schematic.get_expanded_number_map()

    # find every number adjacent to a symbol
    total_gear_ratio = 0
    for symbol_loc, symbol in schematic.symbols.items():
        part_numbers = set()
        # only gears
        if symbol != "*":
            continue
        for adj in get_adjacency_list():
            target = tuple2_add(symbol_loc, adj)
            if target in expanded_number_map:
                part_numbers.add(expanded_number_map[target].number)
        # only two gears
        if len(part_numbers) == 2:
            total_gear_ratio += math.prod(part_numbers)

    return total_gear_ratio


def main() -> None:
    with open("day03_input.txt", "r") as file:
        lines = file.read().splitlines()
        print(part_one(lines))
        print(part_two(lines))


if __name__ == "__main__":
    main()
