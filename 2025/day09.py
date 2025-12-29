import itertools
from collections import deque

from util import Point2D


def parse_lines(lines: list[str]) -> list[tuple[int, int]]:
    return [(int(a), int(b)) for line in lines for a, b in [line.split(",")]]


def part_one(lines) -> int:
    all_reds = parse_lines(lines)
    print(all_reds)
    total = 0
    for pair in itertools.combinations(all_reds, 2):
        total = max(
            total,
            (abs(pair[0][0] - pair[1][0]) + 1) * (abs(pair[0][1] - pair[1][1]) + 1),
        )
    return total


def part_two(lines) -> int:
    def make_bounding_box(rect: tuple[Point2D, Point2D]) -> tuple[Point2D, Point2D]:
        (x1, y1), (x2, y2) = rect
        (x1, y1), (x2, y2) = (min(x1, x2), min(y1, y2)), (max(x1, x2), max(y1, y2))
        return ((x1, y1), (x2, y2))

    def rectangles_intersect(rect1, rect2):
        (x1_min, y1_min), (x1_max, y1_max) = make_bounding_box(rect1)
        (x2_min, y2_min), (x2_max, y2_max) = make_bounding_box(rect2)
        return not (
            x1_max < x2_min or x2_max < x1_min or y1_max < y2_min or y2_max < y1_min
        )

    def render(segments, blue_rectangles, red_rectangles=()):
        import matplotlib.patches as patches
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots(figsize=(12, 8))

        # Draw line segments (list of point pairs)
        for idx, rect in enumerate(segments):
            (x1, y1), (x2, y2) = make_bounding_box(rect)

            # print(f"drawing segment {idx} from {(x1, y1)} to {(x2, y2)}")

            # print(
            #     f"drawing rectangle at {(x1, y1)}, {abs(x2 - x1) + 1}, {abs(y2 - y1) + 1},"
            # )

            ax.add_patch(
                patches.Rectangle(
                    (x1, y1),
                    abs(x2 - x1) + 1,
                    abs(y2 - y1) + 1,
                    facecolor="black",
                    alpha=0.75,
                )
            )

        for rect in blue_rectangles:
            (x1, y1), (x2, y2) = make_bounding_box(rect)
            # print(f"drawing blue rect from {(x1, y1)} to {(x2, y2)}")

            # print(
            #     f"drawing rectangle at {(x1, y1)}, {abs(x2 - x1) + 1}, {abs(y2 - y1) + 1},"
            # )
            ax.add_patch(
                patches.Rectangle(
                    (x1, y1),
                    abs(x2 - x1) + 1,
                    abs(y2 - y1) + 1,
                    facecolor="blue",
                    alpha=0.25,
                )
            )

        for idx, rect in enumerate(reversed(red_rectangles)):
            (x1, y1), (x2, y2) = make_bounding_box(rect)
            ax.add_patch(
                patches.Rectangle(
                    (x1, y1),
                    abs(x2 - x1) + 1,
                    abs(y2 - y1) + 1,
                    facecolor="red" if idx == 0 else "lightgrey",
                    alpha=0.25,
                )
            )

        ax.autoscale()

        if len(segments) < 20:
            ax.set_xticks([0] + [pt[0] for seg in segments for pt in seg])
            ax.set_yticks([0] + [pt[1] for seg in segments for pt in seg])
            ax.tick_params(top=True, bottom=False, labeltop=True, labelbottom=False)

        ax.invert_yaxis()
        ax.set_aspect("equal")
        plt.savefig("day09.png", dpi=300)

    def sort_segment_by_x(seg):
        if seg[0][0] < seg[1][0]:
            return (seg[0], seg[1])
        if seg[0][0] == seg[1][0]:
            if seg[0][1] < seg[1][1]:
                return (seg[0], seg[1])
            else:
                return (seg[1], seg[0])
        else:
            return (seg[1], seg[0])

    def horizontal_segments_overlap(seg1, seg2):
        assert seg1[0][1] == seg1[1][1] and seg2[0][1] == seg2[1][1]
        min_x1 = min(seg1[0][0], seg1[1][0])
        max_x1 = max(seg1[0][0], seg1[1][0])
        min_x2 = min(seg2[0][0], seg2[1][0])
        max_x2 = max(seg2[0][0], seg2[1][0])

        return not (max_x1 <= min_x2 or max_x2 <= min_x1)

    def vertical_ray_intersects_segment(pt: Point2D, seg):
        min_x = min(seg[0][0], seg[1][0])
        max_x = max(seg[0][0], seg[1][0])
        # we're explicitly assuming pt is the left edge
        # so that's why we do the exclusive match on the rhs
        # TODO: We should refactor this so that the pt is explicitly part of the segment
        return min_x <= pt[0] < max_x

    all_reds = parse_lines(lines)
    all_segments = [
        sort_segment_by_x(seg) for seg in itertools.pairwise(all_reds + [all_reds[0]])
    ]

    column_bottoms = {seg[1] for seg in all_segments if seg[0][1] < seg[1][1]}

    min_x = min(pt[0] for pt in all_reds)
    max_x = max(pt[0] for pt in all_reds)
    min_y = min(pt[1] for pt in all_reds)
    max_y = max(pt[1] for pt in all_reds)
    bounding_segments = [
        ((min_x - 5, min_y - 5), (max_x + 5, min_y - 5)),
        ((min_x - 5, max_y + 5), (max_x + 5, max_y + 5)),
    ]
    blue_rectangles = []
    horizontal_segments = [seg for seg in all_segments if seg[0][1] == seg[1][1]]
    horizontal_segments += bounding_segments
    horizontal_segments.sort(key=lambda seg: seg[0][1])

    segments_to_sweep = deque(horizontal_segments)

    while segments_to_sweep:
        seg = segments_to_sweep.popleft()
        left_point, right_point = sort_segment_by_x(seg)
        if right_point in column_bottoms:
            print(f"truncating segment {seg}")
            right_point = (right_point[0] - 1, right_point[1])

        above_intersections = [
            s
            for s in reversed(horizontal_segments)
            if s[0][1] < seg[0][1] and vertical_ray_intersects_segment(left_point, s)
        ]
        below_intersections = [
            s
            for s in horizontal_segments
            if s[0][1] > seg[0][1] and vertical_ray_intersects_segment(left_point, s)
        ]
        print(f"sweeping seg{seg}")
        print(
            f"  above_segments: {above_intersections}, len {len(above_intersections)}"
        )
        print(
            f"  below_segments: {below_intersections}, len {len(below_intersections)}"
        )

        assert (len(above_intersections) % 2 == 1) ^ (len(below_intersections) % 2 == 1)
        if len(above_intersections) % 2 == 0:
            continue
        match_seg = next(
            s
            for s in reversed(horizontal_segments)
            if s[0][1] < seg[0][1]
            and horizontal_segments_overlap((left_point, right_point), s)
        )
        l_match, r_match = sort_segment_by_x(match_seg)
        new_blue = (
            (max(left_point[0], l_match[0]), left_point[1] - 1),
            (min(right_point[0], r_match[0]), r_match[1] + 1),
        )
        print(f"intersecting seg{seg} against match_seg{match_seg}")
        print(f"created blue above: {new_blue}")

        # handle leftover segments
        if l_match[0] > left_point[0]:
            leftover_seg = (
                left_point,
                (l_match[0] - 1, left_point[1]),
            )
            print(f"leftover rhs: {leftover_seg}")
            segments_to_sweep.appendleft(leftover_seg)
        if r_match[0] < right_point[0]:
            leftover_seg = (
                (r_match[0] + 1, left_point[1]),
                right_point,
            )
            print(f"leftover lhs: {leftover_seg}")
            segments_to_sweep.appendleft(leftover_seg)

        blue_rectangles.append(new_blue)
        print(f"total blue rectangles: {blue_rectangles}")
        if len(blue_rectangles) == 2:
            # break
            pass

    total = 0
    red_rectangles = []
    render(all_segments, blue_rectangles, red_rectangles)

    for pair in itertools.combinations(all_reds, 2):
        pair = list(sorted(pair))
        this_size = (abs(pair[0][0] - pair[1][0]) + 1) * (
            abs(pair[0][1] - pair[1][1]) + 1
        )
        red_rect = (
            (min(pair[0][0], pair[1][0]), min(pair[0][1], pair[1][1])),
            (max(pair[0][0], pair[1][0]), max(pair[0][1], pair[1][1])),
        )

        if this_size > total and not any(
            rectangles_intersect(
                rect,
                red_rect,
            )
            for rect in blue_rectangles
        ):
            print(f"new max size {this_size} at points {pair}")
            red_rectangles.append(red_rect)
            total = this_size

    render(all_segments, blue_rectangles, red_rectangles)
    return total


def main() -> None:
    with open("day09_input.txt", "r") as file:
        lines = file.read().splitlines()
        print(part_one(lines))
        print(part_two(lines))


if __name__ == "__main__":
    main()
