import functools
import re
import sys
from collections import defaultdict, deque
from dataclasses import dataclass, field
from functools import cache
from typing import Any, Deque, Dict, List, Set, Tuple, TypeVar

from CharacterGrid import CharacterGrid
from util import Point2D, tuple2_add


def parse_lines(lines: List[str]) -> CharacterGrid:
    return CharacterGrid.from_lines(lines)


@dataclass
class State:
    pos: Point2D
    facing: Point2D
    heat_cost: int
    consecutive_moves: int


def part_one(lines) -> int:
    # n.b.: haven't refactored this function yet, consecutive moves is 'remaining moves'
    grid = parse_lines(lines)
    start_pos = (0, 0)
    best_score = max_int = sys.maxsize
    states_visited = 0

    visit_queue: Deque[State] = deque(
        [
            State(pos=start_pos, facing=(0, 1), consecutive_moves=3, heat_cost=0),
            State(pos=start_pos, facing=(1, 0), consecutive_moves=3, heat_cost=0),
        ]
    )
    visited = defaultdict(
        lambda: defaultdict(lambda: defaultdict(lambda: max_int))
    )  # type:ignore

    # v1
    # Visited states 38877337
    # 1260
    # & c:/windows/py.exe d:/code/advent-of-code/2023/day17.py <=> 4m20s

    # v2: with pruning worse remaining moves
    # Visited states 17232137
    # 1260
    # & c:/windows/py.exe d:/code/advent-of-code/2023/day17.py <=> 2m9s
    # pypy: 1m50s

    # v3: with pruning worse heat scores

    while len(visit_queue) > 0:
        state = visit_queue.pop()
        states_visited += 1
        if states_visited % 1000000 == 0:
            print(f"Visited states {states_visited:,}")

        # test win condition
        if state.pos == (grid.max_x(), grid.max_y()):
            best_score = min(best_score, state.heat_cost)
            continue

        moves = [
            state.facing,
            (state.facing[1], state.facing[0]),
            (-state.facing[1], -state.facing[0]),
        ]

        # a turn is required
        if state.consecutive_moves == 0:
            moves.remove(state.facing)

        for move in moves:
            new_pos = tuple2_add(state.pos, move)

            # bounced off the map
            if new_pos not in grid.map:
                continue

            new_state = State(
                pos=new_pos,
                facing=move,
                heat_cost=state.heat_cost + int(grid.map[new_pos]),
                consecutive_moves=state.consecutive_moves - 1
                if move == state.facing
                else 2,
            )

            # don't go down a road that's already worse
            if new_state.heat_cost > best_score:
                continue

            if (
                visited[new_state.pos][new_state.facing][new_state.consecutive_moves]
                > new_state.heat_cost
            ):
                for moves_left in range(0, new_state.consecutive_moves + 1):
                    visited[new_state.pos][new_state.facing][
                        moves_left
                    ] = new_state.heat_cost
                visit_queue.appendleft(new_state)

    print(f"Visited states {states_visited:,}")
    return best_score


def part_two(lines) -> int:
    grid = parse_lines(lines)
    start_pos = (0, 0)
    best_score = max_int = sys.maxsize
    states_visited = 0

    visit_queue: Deque[State] = deque(
        [
            State(pos=start_pos, facing=(0, 1), consecutive_moves=0, heat_cost=0),
            State(pos=start_pos, facing=(1, 0), consecutive_moves=0, heat_cost=0),
        ]
    )
    visited = defaultdict(
        lambda: defaultdict(lambda: defaultdict(lambda: max_int))
    )  # type:ignore

    # v1

    while len(visit_queue) > 0:
        state = visit_queue.pop()
        states_visited += 1
        if states_visited % 1000000 == 0:
            print(f"Visited states {states_visited:,}")

        # test win condition
        if state.pos == (grid.max_x(), grid.max_y()) and state.consecutive_moves >= 4:
            best_score = min(best_score, state.heat_cost)
            continue

        moves = []
        if state.consecutive_moves <= 9:
            moves.append(state.facing)
        if state.consecutive_moves >= 4:
            moves += [
                (state.facing[1], state.facing[0]),
                (-state.facing[1], -state.facing[0]),
            ]

        for move in moves:
            new_pos = tuple2_add(state.pos, move)

            # bounced off the map
            if new_pos not in grid.map:
                continue

            new_state = State(
                pos=new_pos,
                facing=move,
                heat_cost=state.heat_cost + int(grid.map[new_pos]),
                consecutive_moves=state.consecutive_moves + 1
                if state.facing == move
                else 1,
            )

            # don't go down a road that's already worse
            if new_state.heat_cost > best_score:
                continue

            if (
                visited[new_state.pos][new_state.facing][new_state.consecutive_moves]
                > new_state.heat_cost
            ):
                # todo ultracrucible
                # for moves_left in range(0, new_state.remaining_moves + 1):
                #     visited[new_state.pos][new_state.facing][
                #         moves_left
                #     ] = new_state.heat_cost
                visited[new_state.pos][new_state.facing][
                    new_state.consecutive_moves
                ] = new_state.heat_cost

                visit_queue.appendleft(new_state)

    print(f"Visited states {states_visited:,}")
    return best_score


def main() -> None:
    with open("day17_input.txt", "r") as file:
        lines = file.read().splitlines()
        print(part_one(lines))
        print(part_two(lines))


if __name__ == "__main__":
    main()
