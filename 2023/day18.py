import functools
import re
from collections import defaultdict, deque
from dataclasses import dataclass, field
from functools import cache
from itertools import groupby
from typing import Any, Deque, Dict, List, Set, Tuple, TypeVar

from CharacterGrid import CharacterGrid, Directions, orthogonal_adjacencies
from util import Point2D, tuple2_add, tuple2_scalar_mul

dmap = {
    "U": Directions.UP,
    "D": Directions.DOWN,
    "L": Directions.LEFT,
    "R": Directions.RIGHT,
    "3": Directions.UP,
    "1": Directions.DOWN,
    "2": Directions.LEFT,
    "0": Directions.RIGHT,
}


def parse_lines(lines: List[str]) -> Any:
    result = []
    for line in lines:
        tokens = line.split(" ")
        result.append((tokens[0], tokens[1], tokens[2][2:-1]))

    return result


def part_one(lines) -> int:
    def flood_fill(map: Dict[Point2D, str], loc: Point2D) -> None:
        # permit us to be aggressive with the flood fill
        if map[loc] != ".":
            return

        visited: Set[Point2D] = set()
        queue: Deque[Point2D] = deque()
        queue.append(loc)

        inside = True
        while len(queue) > 0:
            visiting = queue.pop()
            visited.add(visiting)

            for edge in orthogonal_adjacencies:
                target = tuple2_add(visiting, edge)

                if target not in map:
                    inside = False
                    continue

                if target not in visited and target not in queue and map[target] == ".":
                    queue.append(target)

            # if we're adjacent to any edges, we are outside
            # enqueue any adjacent empty spaces

        # finally, color all the spaces
        for pt in visited:
            map[pt] = "I" if inside else "o"

    def mark_inside(map: Dict[Point2D, str], loc: Point2D) -> None:
        ray_trace = "".join(
            [
                # all the pipe segments
                map[(loc[0], y)]
                # from where we are up to y=0
                for y in range(loc[1], -1, -1)
                # only intersect things on the path
                # if distances[(loc[0], y)] != max_int
                # if map[(loc[0], y)] == "#"
            ]
        )
        ray_trace = ray_trace.replace("o", ".")
        # now compress the runs down
        ray_trace = re.sub(r"#{2,}", "", ray_trace)
        ray_trace = re.sub(r"\.+", ".", ray_trace)
        ray_trace = ray_trace.replace(".", "")

        # odd number of intersections means inside
        if (len(ray_trace) % 2) == 1:
            map[loc] = "o"

    lines = parse_lines(lines)

    grid = CharacterGrid(map=defaultdict(lambda: "."))
    digger = (0, 0)
    grid.map[digger] = "#"
    for line in lines:
        (dir_tok, magnitude, color) = line
        for _ in range(int(magnitude)):
            digger = tuple2_add(digger, dmap[dir_tok])
            grid.map[digger] = "#"
        # print(line)
        # grid.render()

    grid.render()

    for x in range(grid.min_x(), grid.width()):
        for y in range(grid.min_y(), grid.height()):
            if grid.map[(x, y)] == ".":
                flood_fill(grid.map, (x, y))

    grid.render()

    return sum(1 for x in grid.map.values() if x not in ("o", "."))


def union_interval_length(intervals: List[Point2D]) -> int:
    if not intervals:
        return 0

    sorted_intervals = list(sorted(intervals))

    result = [sorted_intervals[0]]

    for interval in sorted_intervals[1:]:
        tail = result[-1]
        # we're extending this interval
        if tail[1] == interval[0]:
            result[-1] = (tail[0], interval[1])
        # the interval intersects
        elif tail[0] < interval[0] and tail[1] > interval[1]:
            continue
        # we're truncating the beginning
        elif tail[0] == interval[0] and interval[1] != tail[1]:
            result[-1] = (tail[0], interval[1])
        # we're truncating the end
        elif tail[0] < interval[0] and interval[1] == tail[1]:
            continue
        else:
            result.append(interval)

    totes = sum(x[1] - x[0] + 1 for x in result)
    print(f"\tUnioned intervals: {result}, we have {totes}")

    return totes


def coalesce_intervals(intervals: List[Point2D]) -> Tuple[List[Point2D], int]:
    if not intervals:
        return (list(), 0)

    # Sort intervals based on start values
    sorted_intervals = list(sorted(intervals))
    print(f"\tCoalescing {sorted_intervals}")

    result = [sorted_intervals[0]]
    extra_width = 0

    for interval in sorted_intervals[1:]:
        tail = result[-1]
        # we're extending this interval
        if tail[1] == interval[0]:
            result[-1] = (tail[0], interval[1])
        # the interval intersects
        elif tail[0] < interval[0] and tail[1] > interval[1]:
            result[-1] = (tail[0], interval[0])
            result.append((interval[1], tail[1]))
            extra_width += interval[1] - interval[0]
        # we're truncating the beginning
        elif tail[0] == interval[0] and interval[1] != tail[1]:
            result[-1] = (tail[1], interval[1])
            extra_width += tail[1] - tail[0]
        # we're truncating the end
        elif tail[0] < interval[0] and interval[1] == tail[1]:
            result[-1] = (tail[0], interval[0])
        elif tail == interval:
            # count the entire interval, because this is the only time we see it
            # inclusive
            extra_width += (interval[1] - interval[0]) + 1
            del result[-1]

        else:
            # No overlap, add the interval to the result
            result.append(interval)
        print(f"\tAfter {interval}, we have {result}")

    return (result, extra_width)


def parse_colored_lines(lines: List[str]) -> List[Tuple[Point2D, Point2D]]:
    # parse the input into strokes
    strokes = []
    for line in parse_lines(lines):
        (_, _, color) = line
        dir = dmap[color[-1]]
        length = int(color[:-1], 16)
        strokes.append((dir, length))
        # print(f"dir: {dir} length: {length}")
    start = (0, 0)
    # now turn the strokes into segments
    segments = []
    for stroke in strokes:
        end = tuple2_add(start, tuple2_scalar_mul(stroke[0], stroke[1]))
        segments.append((start, end))
        start = end

    # we better get back to start
    assert start == (0, 0)
    return segments


def parse_regular_lines(lines: List[str]) -> List[Tuple[Point2D, Point2D]]:
    # lines = parse_lines(lines)
    # parse the input into strokes

    strokes = []
    for line in parse_lines(lines):
        (dir, length, _) = line
        # dir = dmap[color[-1]]
        # length = int(color[:-1], 16)
        strokes.append((dmap[dir], int(length)))
        # print(f"dir: {dir} length: {length}")
    start = (0, 0)
    # now turn the strokes into segments
    segments = []
    for stroke in strokes:
        end = tuple2_add(start, tuple2_scalar_mul(stroke[0], stroke[1]))
        segments.append((start, end))
        start = end

    # we better get back to start
    assert start == (0, 0)
    return segments


def part_two(lines, legacy: bool = False) -> int:
    if legacy:
        segments = parse_regular_lines(lines)
    else:
        segments = parse_colored_lines(lines)

    for segment in segments:
        print(f"{segment[0]} -> {segment[1]}")

    # alright time to start counting
    horizontal_slices = filter(lambda seg: seg[0][1] == seg[1][1], segments)
    by_y = groupby(
        sorted(horizontal_slices, key=lambda s: s[0][1]), lambda seg: seg[0][1]
    )

    total_dug = 0

    open_intervals: List[Point2D] = []
    prev_y = None
    for y, segs in by_y:
        # accumulate width * dy
        if prev_y is not None:
            width = sum(1 + x[1] - x[0] for x in open_intervals)
            print(
                f"{total_dug} + {width} * ({y}-{prev_y}-1) = {total_dug + width * (y - prev_y -1)}"
            )
            total_dug += width * (y - prev_y - 1)

        # we don't need the y anymore
        x_intervals: List[Point2D] = [
            tuple(sorted((seg[0][0], seg[1][0]))) for seg in segs  # type:ignore
        ]
        print(f"{y}: {x_intervals}")
        this_row_width = 0
        for i in x_intervals:
            if i in open_intervals:
                open_intervals.remove(i)
                # still counts
                this_row_width += (i[1] - i[0]) + 1
            else:
                open_intervals.append(i)

        extra_width = union_interval_length(open_intervals)
        (open_intervals, _) = coalesce_intervals(open_intervals)  # type: ignore
        this_row_width += extra_width
        print(f"Open status: {open_intervals}")

        print(
            f"Adding this row's width. {this_row_width}. Total now {total_dug +  this_row_width}"
        )
        total_dug += this_row_width

        prev_y = y

    return total_dug


def main() -> None:
    with open("day18_input.txt", "r") as file:
        lines = file.read().splitlines()
        print(part_one(lines))
        print(part_two(lines))


if __name__ == "__main__":
    main()
