import copy
import functools
import re
from collections import deque
from dataclasses import dataclass, field
from functools import cache
from typing import Any, Dict, List, Tuple, TypeVar

Tuple4 = Tuple[int, int, int, int]


def tuple4_add(a: Tuple4, b: Tuple4) -> Tuple4:
    return tuple(map(sum, zip(a, b)))  # type: ignore


@dataclass
class Blueprint:
    costs: List[List[int]]
    # ore_ore: int
    # clay_ore: int
    # obsidian_ore: int
    # obsidian_clay: int
    # geode_ore: int
    # geode_obsidian: int


# @dataclass
# class GameState:
#     # robots: Tuple[int, int, int, int] = (1, 0, 0, 0)
#     # mats: Tuple[int, int, int, int] = (0, 0, 0, 0)
#     robots: List[int] = field(default_factory=lambda: [1, 0, 0, 0])
#     mats: List[int] = field(default_factory=lambda: [0, 0, 0, 0])


def parse_lines(lines: List[str]) -> List[Blueprint]:
    blueprints: List[Blueprint] = []
    for line in lines:
        # Blueprint 1:  Each ore robot costs 4 ore.  Each clay robot costs 2 ore.  Each obsidian robot costs 3 ore and 14 clay.  Each geode robot costs 2 ore and 7 obsidian.
        line = line.strip()
        if match := re.search(
            r"Blueprint \d+: Each ore robot costs (\d+) ore. Each clay robot costs (\d+) ore. Each obsidian robot costs (\d+) ore and (\d+) clay. Each geode robot costs (\d+) ore and (\d+) obsidian.",
            line,
        ):
            (
                ore_ore,
                clay_ore,
                obsidian_ore,
                obsidian_clay,
                geode_ore,
                geode_obsidian,
            ) = match.groups()
            # costs =
            blueprints.append(
                Blueprint(
                    [
                        [-int(ore_ore), 0, 0, 0],
                        [-int(clay_ore), 0, 0, 0],
                        [-int(obsidian_ore), -int(obsidian_clay), 0, 0],
                        [-int(geode_ore), 0, -int(geode_obsidian), 0],
                    ]
                )
            )
        else:
            raise AssertionError(f"could not parse: [{line}]")

    return blueprints


commands = ["o", "c", "z", "g", "."]

verbose = False
verify_simulate = False
v2_robot_maxes = True


@dataclass
class GameState:
    robots: Tuple[int, int, int, int]
    mats: Tuple[int, int, int, int]
    minute_finished: int
    movestring: str


def find_max_score(bp: Blueprint, minutes: int) -> int:
    max_geodes: int = 0
    best_move: str
    count_iterations = 0

    queue = deque([GameState((1, 0, 0, 0), (0, 0, 0, 0), 0, "")])

    while len(queue) > 0:
        count_iterations += 1
        today = queue.popleft()
        if count_iterations % 50000 == 0:
            print(
                f"Iteration {count_iterations}. Queue depth {len(queue)}. Max score {max_geodes}. Processing day ={today.minute_finished+1}"
            )
            print(
                f"robots: {today.robots} mats = {today.mats} moves = {today.movestring}"
            )

        # process today
        start_of_day_mats = today.mats
        today.mats = tuple4_add(today.robots, today.mats)
        today_score = today.mats[-1]
        max_geodes = max(max_geodes, today_score)
        if today_score == max_geodes:
            best_move = today.movestring
        today.minute_finished += 1

        # self-verify
        if verify_simulate:
            simulated_score = simulate(
                today.movestring + ".", bp, today.minute_finished
            )
            if simulated_score != today_score:
                raise AssertionError(
                    f"Simulated score {simulated_score} != today score {today_score}"
                )

        # are we done, return scores?
        if today.minute_finished == minutes:
            continue

        robot_budgets = [0, 0, 0]

        robot_budgets[2] = -bp.costs[3][2] - today.robots[2]

        # we only need enough clay to make obsidian robots
        # and if we have all our obsidian robots, we don't even need that
        robot_budgets[1] = (
            0 if robot_budgets[2] <= 0 else -bp.costs[2][1]
        ) - today.robots[1]

        # we need enough ore to build clay or obsidian maybe
        robot_budgets[0] = (
            max(
                0 if robot_budgets[2] <= 0 else -bp.costs[2][0],
                0 if robot_budgets[1] <= 0 else -bp.costs[1][0],
            )
            - today.robots[0]
        )

        # v2, include mat stockpiles
        # if we want one robot, we need x on hand
        # if we want 2 robots, we need x on hand an
        if v2_robot_maxes:
            if today.mats[2] > -bp.costs[3][2] * (minutes - today.minute_finished):
                robot_budgets[2] = 0

            if today.mats[1] > -bp.costs[2][1] * robot_budgets[2]:
                robot_budgets[1] = 0

            if today.mats[0] > (
                (-bp.costs[3][0] * (minutes - today.minute_finished))
                + (-bp.costs[2][0] * robot_budgets[2])
                + (-bp.costs[1][0] * robot_budgets[1])
            ):
                robot_budgets[0] = 0

        # there are five moves we could make
        options_tested = 0
        for cmd_index in (3, 2, 1, 0):
            command = commands[cmd_index]
            tomorrow = copy.copy(today)
            # todo cleanup
            # tomorrow.movestring += command

            # we don't even want any more of this robot
            if cmd_index in (0, 1, 2) and robot_budgets[cmd_index] <= 0:
                continue

            # not only can we not afford these robots, we can't sleep
            # long enough to afford them
            if cmd_index == 2 and today.robots[1] == 0:
                continue
            if cmd_index == 3 and today.robots[2] == 0:
                continue
            # production_check
            # days_needed = todo
            # don't ever sleep away the last day (we need it to count score)
            # days_remaining = (tomorrow.minute_finished - minutes) - 1

            # if we made it, then do build the robot
            # spend the money
            # retroactive_mats = tuple4_add(bp.costs[cmd_index], start_of_day_mats)  # type: ignore

            # sleep until we have enough or we run out of days
            # print(
            #     f"Iteration {count_iterations}. Queue depth {len(queue)}. Max score {max_geodes}. Processing day ={today.minute_finished+1}"
            # )
            # print(
            #     f"robots: {today.robots} mats = {today.mats} moves = {today.movestring}"
            # )

            # print(f"Attempting to build {command}")
            retroactive_mats = start_of_day_mats
            while (
                any(
                    map(
                        lambda m: m < 0,
                        # map(sum, zip(bp.costs[cmd_index], start_of_day_mats)),
                        tuple4_add(bp.costs[cmd_index], retroactive_mats),  # type: ignore
                    )
                )
                and tomorrow.minute_finished < minutes - 1
            ):
                # print(f"sleeping..")
                # spend a day
                # inject the sleeps: increment mats, increment clock, increment movestring
                tomorrow.mats = tuple4_add(today.robots, tomorrow.mats)
                retroactive_mats = tuple4_add(today.robots, retroactive_mats)
                tomorrow.minute_finished += 1
                tomorrow.movestring += "."
            # print("Done")
            # while any(map(lambda m: m < 0, retroactive_mats)) and tomorrow.minute_finished < minutes-1:

            # pass

            # ok, how many days would it take at this rate
            # if our production is offline, don't even sleep
            # if we don't have enough days, just inject enough
            # sleeps so that the last day runs
            # if we do have enough days, inject enough sleeps
            # to get us t
            # do we have enough days to inject sleeps?
            # continue
            # if we were able to sleep enough days, go for it
            # if days_needed <= days_remaining:
            if all(
                map(
                    lambda m: m >= 0,
                    # map(sum, zip(bp.costs[cmd_index], start_of_day_mats)),
                    tuple4_add(bp.costs[cmd_index], retroactive_mats),  # type: ignore
                )
            ):
                tomorrow.movestring += command
                # pay the cost
                tomorrow.mats = tuple4_add(bp.costs[cmd_index], tomorrow.mats)  # type: ignore

                # build the robot
                tomorrow.robots = tuple(
                    (n + 1 if i == cmd_index else n for i, n in enumerate(today.robots))
                )  # type:ignore
            else:
                # print("We slept too long and couldn't build the robot")
                tomorrow.movestring += "."

            # ship it
            queue.append(tomorrow)
            options_tested += 1
            # only test the best two options
            # if options_tested == 2:
            # break

    print(
        f"Terminating after {count_iterations} with best score {max_geodes} example [{best_move}]"
    )
    return max_geodes


def simulate(solution: str, bp: Blueprint, minutes: int) -> int:
    robots: List[int] = [1, 0, 0, 0]
    mats: List[int] = [0, 0, 0, 0]

    print(f"Simulating [{solution}] of length {len(solution)}")

    assert len(solution) == minutes
    for minute in range(1, minutes + 1):
        command_char = solution[minute - 1]
        command = commands.index(command_char)
        sleeping = command == len(commands) - 1
        if sleeping:
            if verbose:
                print(f"Minute {minute}:(sleeping):")
        else:
            # build robot N
            if verbose:
                print(
                    f"Minute {minute}:[{command_char}]: Building robot {command} for cost {bp.costs[command]}"
                )

        # consume cost
        if not sleeping:
            for i in range(len(bp.costs[command])):
                mats[i] += bp.costs[command][i]
        # test negative
        assert all(map(lambda m: m >= 0, mats))
        # process robots
        for i in range(len(robots)):
            mats[i] += robots[i]
        # build new robot

        if not sleeping:
            robots[command] += 1
        if verbose:
            print(f"End of minute {minute}: robots = {robots}, mats = {mats}")

    # at end of final minute emit geodes
    return mats[3]


def part_one(lines) -> int:
    bps = parse_lines(lines)
    total_quality = 0
    for idx, bp in enumerate(bps):
        score = find_max_score(bp, 24)
        total_quality += (idx + 1) * score
    return total_quality


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
