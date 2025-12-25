import functools
import heapq
import re
from collections import defaultdict
from dataclasses import dataclass, field
from functools import cache

from _interpchannels import close

from util import Point3D


def parse_lines(lines: list[str]) -> list[Point3D]:
    return list(sorted(tuple(map(int, line.split(","))) for line in lines))


def part_one(lines) -> int:
    points = parse_lines(lines)
    connections = 10 if len(points) == 20 else 1000
    # distances = {}
    distance_heap = []
    for idx, pt in enumerate(points):
        for idx2 in range(idx + 1, len(points)):
            pt2 = points[idx2]
            # distances[(pt, pt2)] = sum(pow(x - y, 2) for x, y in zip(pt, pt2))
            heapq.heappush(
                distance_heap, (sum(pow(x - y, 2) for x, y in zip(pt, pt2)), (pt, pt2))
            )
            # distances[(pt2, pt)] = distances[(pt, pt2)]

    # distance_heap = heapq.heapify((v, k) for k, v in distances.items())
    # circuits = {}
    # print(heapq.heappop(distance_heap))
    pairs = []
    for c in range(connections):
        distance, pair = heapq.heappop(distance_heap)
        pairs.append(pair)
    print(f"Pairs: {len(pairs)}")

    edges = defaultdict(set)
    for a, b in pairs:
        edges[a].add(b)
        edges[b].add(a)

    # print(f"Making a set of {len(points)}")
    to_visit = set(points)
    visited = set()
    subgraphs = []
    # print(f"  {len(to_visit)} points left to visit")
    while to_visit:
        # print(f"Starting new graph at {start}, count of graphs now {len(subgraphs)}")
        # print(f"  {len(to_visit)} points left to visit")
        stack = [to_visit.pop()]
        subgraph_size = 0
        while stack:
            node = stack.pop()
            visited.add(node)
            subgraph_size += 1
            # print(f"Visiting node {node}, {len(visited)} visited so far")
            for neighbor in edges[node]:
                if neighbor not in visited and neighbor not in stack:
                    stack.append(neighbor)
                    to_visit.discard(neighbor)
                    # print(f"  Pushing neighbor {neighbor} to stack of len {len(stack)}")
        subgraphs.append(subgraph_size)
        # print(f"Closing graph {len(subgraphs)} the set of size {subgraphs[-1]}")
    subgraphs.sort(reverse=True)
    # print(f"Subgraphs: {subgraphs}")
    return subgraphs[0] * subgraphs[1] * subgraphs[2]


def part_two(lines) -> int:
    parse_lines(lines)
    total = 0
    return total


def main() -> None:
    with open("day08_input.txt", "r") as file:
        lines = file.read().splitlines()
        print(part_one(lines))
        print(part_two(lines))


if __name__ == "__main__":
    main()
