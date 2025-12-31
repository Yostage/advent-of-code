from collections import defaultdict, deque
from functools import lru_cache


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
    stack = deque()
    stack.appendleft(path)
    while stack:
        path = stack.pop()
        current = path[-1]
        for neighbor in edges[current]:
            stack.appendleft(path + (neighbor,))
            if neighbor == "out":
                total += 1
    return total


global_edges = {}


@lru_cache
def recursive_paths_to_dest(src, dest, current) -> int:
    return sum(
        (1 if neighbor == dest else recursive_paths_to_dest(src, dest, neighbor))
        for neighbor in global_edges[current]
    )


def part_two(lines):
    graph = parse_lines(lines)
    edges = defaultdict(set)
    for src, dsts in graph:
        for dst in dsts:
            edges[src].add(dst)
    global global_edges
    global_edges = edges
    return (
        recursive_paths_to_dest("svr", "fft", "svr")
        * recursive_paths_to_dest("fft", "dac", "fft")
        * recursive_paths_to_dest("dac", "out", "dac")
    )


def graphviz(lines):
    graph = parse_lines(lines)
    for src, dsts in graph:
        for dst in dsts:
            print(f"  {src} -> {dst};")


def main() -> None:
    with open("day11_input.txt", "r") as file:
        lines = file.read().splitlines()
        # 749
        print(part_one(lines))
        print(part_two(lines))


if __name__ == "__main__":
    main()
