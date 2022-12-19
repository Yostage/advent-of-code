import re
from typing import List, Optional

from more_itertools import batched, take


def cratelines_to_crates(lines):
    # how many crates are there
    num_crates = len(lines[0])
    crates = [[] for _ in range(num_crates)]
    # started from the bottom now we here
    for crateline in reversed(lines):
        for idx, x in enumerate(crateline):
            if x is None:
                continue
            else:
                crates[idx].append(x)

    return crates


def execute_move(crates: List[List[int]], move: List[int]) -> None:
    print(f"Crates: {crates}")
    print(f"Executing move: {move}")
    (num_crates, src, dest) = move
    # 1 indexed
    for _ in range(num_crates):
        crates[dest - 1].append(crates[src - 1].pop())


def execute_move_v2(crates: List[List[int]], move: List[int]) -> None:
    print(f"Crates: {crates}")
    print(f"Executing move: {move}")
    (num_crates, src, dest) = move

    # 1 indexed
    # slice the chunk off the end of the dest, put it on the src, then delete it
    crates[dest - 1] += crates[src - 1][-num_crates:]
    del crates[src - 1][-num_crates:]


def parse_input(lines: List[str]):
    top_down_crates = []
    moves = []
    lineiter = iter(lines)
    for line in lineiter:
        if line[1] != "1":
            top_down_crates.append(parse_crateline(line))
        else:
            break

    # n.b. splitlines will eliminate the empty line, so we only need to skip the crate counter
    take(1, lineiter)

    for line in lineiter:
        moves.append(parse_instructions(line))

    return (top_down_crates, moves)


# parse one line of crate stuff and return a sparse vector of crates
def parse_crateline(line: str) -> List[Optional[str]]:
    middles: List[Optional[str]] = [chunk[1] for chunk in batched(iter(line), 4)]
    middles = [None if m == " " else m for m in middles]
    return middles


def parse_instructions(line: str) -> List[int]:
    m = re.search(r"move (\d+) from (\d+) to (\d+)", line)
    assert m is not None
    moves = list(m.groups())
    return [int(m) for m in moves]

    # just take it in chunks of 4 and read out the
    # [X] [X] [X]
    # 111122223333
    # return ["N", None]


def part_one(lines):
    (top_down_crates, moves) = parse_input(lines)
    crates = cratelines_to_crates(top_down_crates)
    for move in moves:
        execute_move(crates, move)
    return [crate[-1] for crate in crates]


def part_two(lines):
    (top_down_crates, moves) = parse_input(lines)
    crates = cratelines_to_crates(top_down_crates)
    for move in moves:
        execute_move_v2(crates, move)
    return [crate[-1] for crate in crates]


def main():
    with open("day5_input.txt", "r") as file:
        lines = file.read().splitlines()

    print(part_two(lines))


if __name__ == "__main__":
    main()
