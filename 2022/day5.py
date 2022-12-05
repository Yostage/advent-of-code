import functools
import itertools
import re
from typing import Iterator, List


def grouper(iterator: Iterator, n: int) -> Iterator[list]:
    while chunk := list(itertools.islice(iterator, n)):
        yield chunk


def take(iterable, n):
    "Return first n items of the iterable as a list"
    return list(itertools.islice(iterable, n))


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
    take(lineiter, 1)

    for line in lineiter:
        moves.append(parse_instructions(line))

    return (top_down_crates, moves)


# parse one line of crate stuff and return a sparse vector of crates
def parse_crateline(line: str) -> List[str]:
    middles = [chunk[1] for chunk in grouper(iter(line), 4)]
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


def main():
    with open("day5_input.txt", "r") as file:
        lines = file.read().splitlines()

        # intervalList = [
        #     input_string_to_intervals(line) for line in file.read().splitlines()
        # ]
        # matches = [1 if intervals_overlap(i) else 0 for i in intervalList]
        # print(sum(matches))


if __name__ == "__main__":
    main()
