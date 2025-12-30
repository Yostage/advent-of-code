import functools
import re
import time
from dataclasses import dataclass, field
from functools import cache
from itertools import combinations

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp


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
        joltage_ratings = list(map(int, joltage_text[1:-1].split(",")))
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


def min_presses_indicator_lights(switch) -> int:
    (output_lights, switch_toggles, _) = switch

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
    raise RuntimeError(f"No solution found for output lights {output_lights}")


def part_one(lines) -> int:
    switches = parse_lines(lines)
    # print(output_lights, switch_toggles, joltage_ratings)

    return sum(min_presses_indicator_lights(switch) for switch in switches)


def min_presses_joltage(switch) -> int:
    (_, switch_toggles, joltage_ratings) = switch
    start_time = time.time()
    distributions_tested = 0
    for presses in range(max(joltage_ratings), sum(joltage_ratings) + 1):
        for distribution in distributions(presses, len(switch_toggles)):
            distributions_tested += 1
            if distributions_tested % 5000000 == 0:
                current_time = time.time()
                print(
                    f" Tested {distributions_tested} distributions in {current_time - start_time:.2f} seconds"
                )
            # Apply this distribution of presses
            joltage_state = [0] * len(joltage_ratings)
            for toggle_idx, press_count in enumerate(distribution):
                for light_idx in switch_toggles[toggle_idx]:
                    joltage_state[light_idx] += press_count
            if joltage_state == joltage_ratings:
                print(
                    f"Found solution with presses={presses} for joltage_ratings={joltage_ratings}"
                )
                endtime = time.time()
                print(
                    f" Tested {distributions_tested} distributions in {endtime - start_time:.2f} seconds"
                )
                print(
                    f" Distributions per second: {distributions_tested / (endtime - start_time)}"
                )
                return presses
            # else:
            #     print(
            #         f"  Tried presses={presses} distribution={distribution} got {joltage_state}"
            #     )
    raise RuntimeError(f"No solution found for joltage ratings {joltage_ratings}")


def min_presses_joltage_scipy(switch) -> int:

    (_, switch_toggles, joltage_ratings) = switch
    switch_toggles_array = np.zeros(
        (len(switch_toggles), len(joltage_ratings)), dtype=int
    )
    for toggle_idx, toggle in enumerate(switch_toggles):
        for light_idx in toggle:
            switch_toggles_array[toggle_idx, light_idx] = 1

    A = switch_toggles_array
    B = np.array(joltage_ratings)
    n_vars = A.shape[0]  # 6 items

    result = milp(
        c=np.ones(n_vars),  # minimize sum(X)
        constraints=LinearConstraint(A.T, B, B),
        integrality=np.ones(n_vars),  # all integers
        bounds=Bounds(lb=0, ub=max(joltage_ratings)),
    )
    assert result.success
    assert result.status == 0
    # print(f"{result.x} : sum:{int(sum(result.x))}, fun:{result.fun}")
    return round(result.fun)


def part_two(lines) -> int:
    switches = parse_lines(lines)
    return sum(min_presses_joltage_scipy(switch) for switch in switches)


def main() -> None:
    with open("day10_input.txt", "r") as file:
        lines = file.read().splitlines()
    print(part_one(lines))
    print(part_two(lines))


if __name__ == "__main__":
    main()
