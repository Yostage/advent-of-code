import functools
import re
from dataclasses import dataclass, field
from functools import cache
from itertools import combinations


def parse_lines(lines: list[str]):
    switches = []
    for line in lines:
        bits = line.split()
        (output_lights_text, switch_toggles_text, joltage_text) = (
            bits[0],
            bits[1:-1],
            bits[-1],
        )
        output_lights = [c == "#" for c in output_lights_text[1:-1]]
        switch_toggles = [
            tuple(map(int, toggle[1:-1].split(","))) for toggle in switch_toggles_text
        ]
        joltage_ratings = joltage_text[1:-1].split(",")
        # print(output_lights, switch_toggles, joltage_ratings)
        switches.append((output_lights, switch_toggles, joltage_ratings))

    return switches


def distributions(n, k):
    """Generate all ways to distribute n items into k slots."""
    # Place k-1 dividers among n+k-1 positions
    for dividers in combinations(range(n + k - 1), k - 1):
        result = []
        prev = -1
        for d in dividers:
            result.append(d - prev - 1)
            prev = d
        result.append(n + k - 2 - prev)
        yield tuple(result)


def min_presses(switch) -> int:
    (output_lights, switch_toggles, joltage_ratings) = switch

    for presses in range(len(switch_toggles) + 1):
        for distribution in distributions(presses, len(switch_toggles)):
            # Apply this distribution of presses
            lights_state = [False] * len(output_lights)
            for toggle_idx, press_count in enumerate(distribution):
                if press_count % 2 == 1:
                    # Toggle this switch
                    for light_idx in switch_toggles[toggle_idx]:
                        lights_state[light_idx] = not lights_state[light_idx]
            if lights_state == output_lights:
                return presses

    # num_lights = len(output_lights)
    # presses = 0
    # for light_idx in range(num_lights):
    #     if output_lights[light_idx]:
    #         # Need this light ON
    #         toggle_idxs = [
    #             idx
    #             for idx, toggle in enumerate(switch_toggles)
    #             if light_idx in toggle
    #         ]
    #         if not toggle_idxs:
    #             # No way to turn this light on
    #             return float("inf")
    #         # Choose the toggle with the lowest joltage rating
    #         best_toggle_idx = min(
    #             toggle_idxs,
    #             key=lambda idx: int(joltage_ratings[idx]),
    #         )
    #         presses += int(joltage_ratings[best_toggle_idx])
    return presses


def part_one(lines) -> int:
    switches = parse_lines(lines)
    # print(output_lights, switch_toggles, joltage_ratings)

    return sum(min_presses(switch) for switch in switches)


def part_two(lines) -> int:
    parse_lines(lines)
    total = 0
    return total


def main() -> None:
    with open("day10_input.txt", "r") as file:
        lines = file.read().splitlines()
        print(part_one(lines))
        print(part_two(lines))


if __name__ == "__main__":
    main()
