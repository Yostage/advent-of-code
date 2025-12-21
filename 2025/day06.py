import itertools
import re
from collections import defaultdict
from typing import Deque, List

from CharacterGrid import CharacterGrid


def parse_lines(lines: List[str]) -> List[str]:
    return lines


def part_one(lines) -> int:
    lines = parse_lines(lines)
    total = 0
    cols = defaultdict(Deque)
    for line in lines:
        for i, c in enumerate(line.split()):
            cols[i].append(c)

    for col in cols.values():
        op = col.pop()
        column_total = int(col.popleft())
        while col:
            val = col.popleft()
            if op == "*":
                column_total *= int(val)
            elif op == "+":
                column_total += int(val)
        total += column_total

    return total


def part_two(lines) -> int:
    lines = parse_lines(lines)

    op_line = lines[-1]
    print("[" + op_line + "]")
    op_chunks = re.split(r"(\*|\+)", op_line)
    assert len(op_chunks) % 2 == 1
    # op_chunks = op_chunks[1:]
    op_and_spaces = [pair[0] + pair[1] for pair in itertools.batched(op_chunks[1:], 2)]
    # because i can't figure out how to split correctly
    op_and_spaces[-1] += " "
    # print(op_and_spaces)

    total = 0
    # cols = defaultdict(Deque)
    # use the bottom line to determine the size of each box
    #
    index = 0
    for op_and_space in op_and_spaces:
        print(op_and_space)
        subgrid = [line[index : index + len(op_and_space) - 1] for line in lines[:-1]]
        # print(subgrid)
        map = CharacterGrid.from_lines(subgrid)
        numbers = [int(map.get_column_string(x)) for x in range(map.width())]
        print(numbers)
        column_total = numbers[0]
        op = op_and_space[0]
        for number in numbers[1:]:
            if op == "*":
                column_total *= number
            elif op == "+":
                column_total += number
        print(f"{op.join([str(n) for n in reversed(numbers)])} = {column_total}")
        # print(column_total)
        total += column_total

        # print(numbers)
        # map.render()
        index += len(op_and_space)
        #
    # for line in lines:
    # print(line)
    # for i, c in enumerate(line.split()):
    # cols[i].append(c)

    # for i, col in cols:

    # for col in cols.values():
    #     op = col.pop()
    #     column_total = int(col.popleft())
    #     while col:
    #         val = col.popleft()
    #         if op == "*":
    #             column_total *= int(val)
    #         elif op == "+":
    #             column_total += int(val)
    #     total += column_total

    return total


def main() -> None:
    with open("day06_input.txt", "r") as file:
        lines = file.read().splitlines()
        print(part_one(lines))
        print(part_two(lines))


if __name__ == "__main__":
    main()
