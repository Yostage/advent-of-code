import functools
import re
from collections import defaultdict, deque
from dataclasses import dataclass, field
from functools import cache


def parse_lines(lines: list[str]) -> list[tuple[str, list[str]]]:
    out = []
    for line in lines:
        (left, right) = line.split(": ")
        out.append((left, right.split()))

    return out


def part_one(lines) -> int:
    graph = parse_lines(lines)
    edges = defaultdict(set)
    for src, dsts in graph:
        for dst in dsts:
            edges[src].add(dst)
    total = 0
    path = ("you",)
    visited = set()
    stack = deque()
    stack.appendleft((path, visited))
    while stack:
        (path, visited) = stack.pop()
        current = path[-1]
        visited.add(current)

        for neighbor in edges[current]:
            if neighbor in visited:
                continue
            stack.appendleft((path + (neighbor,), visited.copy()))
            if neighbor == "out":
                total += 1
                print(f"Path {total}: {path}")

    return total


def part_two(lines) -> int:
    parse_lines(lines)
    total = 0
    return total


def main() -> None:
    with open("day11_input.txt", "r") as file:
        lines = file.read().splitlines()
        print(part_one(lines))
        print(part_two(lines))


if __name__ == "__main__":
    main()
