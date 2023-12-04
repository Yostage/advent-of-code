import functools
import re
from dataclasses import dataclass, field
from functools import cache
from typing import Any, Dict, List, TypeVar


def parse_lines(lines: List[str]) -> Any:
    # Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
    rows = []
    for line in lines:
        the_rest = line.split(":")[1][1:]
        rows.append(
            [
                {
                    color_ball.split(" ")[1]: int(color_ball.split(" ")[0])
                    for color_ball in subset.split(", ")
                }
                for subset in the_rest.split("; ")
            ]
        )
    # print(rows)
    return rows


def part_one(lines) -> int:
    def test_subset_against_bag(subset, bag) -> bool:
        return all(bag[color] >= balls for color, balls in subset.items())

    def test_game_against_bag(game, bag) -> bool:
        return all(test_subset_against_bag(subset, bag) for subset in game)

    bag = {"red": 12, "green": 13, "blue": 14}
    games = parse_lines(lines)

    return sum(
        (idx + 1) for idx, game in enumerate(games) if test_game_against_bag(game, bag)
    )


def part_two(lines) -> int:
    def get_game_power(game) -> int:
        red = max([subset.get("red", 0) for subset in game])
        green = max([subset.get("green", 0) for subset in game])
        blue = max([subset.get("blue", 0) for subset in game])
        return red * green * blue

    games = parse_lines(lines)
    return sum(get_game_power(game) for game in games)


def main() -> None:
    with open("day02_input.txt", "r") as file:
        lines = file.read().splitlines()
        print(part_one(lines))
        print(part_two(lines))


if __name__ == "__main__":
    main()
