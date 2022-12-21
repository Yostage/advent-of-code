import functools
import re
from collections import deque
from dataclasses import dataclass, field
from functools import cache
from typing import Any, Dict, Iterable, List, Set, Tuple, TypeVar


class CallCounter(object):
    "Decorator that keeps track of the number of times a function is called."

    __instances = {}  # type: ignore

    def __init__(self, f):
        self.__f = f
        self.__numcalls = 0
        CallCounter.__instances[f] = self

    def __call__(self, *args, **kwargs):
        self.__numcalls += 1
        return self.__f(*args, **kwargs)

    # @staticmethod
    def count_calls(self):
        "Return the number of times the function f was called."
        return CallCounter.__instances[self.__f].__numcalls

    @staticmethod
    def clear():
        for f in CallCounter.__instances:
            CallCounter.__instances[f].__numcalls = 0

    @staticmethod
    def counts():
        "Return a dict of {function: # of calls} for all registered functions."
        return dict(
            [
                (f.__name__, CallCounter.__instances[f].__numcalls)
                for f in CallCounter.__instances
            ]
        )


@dataclass
class Valve:
    name: str
    flow_rate: int
    edge_string: str
    edges: Set["Valve"]

    def __key(self):
        return (self.name, self.flow_rate)

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        if isinstance(other, Valve):
            return self.__key() == other.__key()
        return NotImplemented


ValveDict = Dict[str, Valve]


def parse_lines(lines: List[str]) -> ValveDict:
    valves: Dict[str, Valve] = {}
    for line in lines:
        if match := re.search(
            r"Valve (.*) has flow rate=(\d+); tunnels? leads? to valves? (.*)", line
        ):
            (name, flow, edges) = match.groups()
            valves[name] = Valve(
                name=name, flow_rate=int(flow), edge_string=edges, edges=set()
            )
        else:
            raise AssertionError(f"could not parse: {line}")

    # hook up all edges
    for valve in valves.values():
        for edge in valve.edge_string.split(", "):
            valve.edges.add(valves[edge])

    return valves


def print_graph(v: ValveDict) -> None:
    edges: Set[str] = set()
    for valve in v.values():
        for edge in valve.edges:
            e = list(sorted([valve.name, edge.name]))
            # mermaid
            # edges.add(f"{e[0]} <--> {e[1]}")
            # graphviz
            edges.add(f"{e[0]} -> {e[1]} [dir=both];")

    for edge_str in edges:
        print(edge_str)


# at each iteration we can remove nodes from the graph if the graph is still
# connected without it
# but what about this one
# 10-1-1-0-1-1-10


# at each point, we will only visit one new node
# we will visit that node by the cheapest path
# so that's the recursion

# visits = 0


bfs_cache: Dict[Tuple[str, str], int] = {}


@CallCounter
def bfs_shortest_distance(valves: ValveDict, start_at: str, dest: str) -> int:
    if (start_at, dest) in bfs_cache:
        return bfs_cache[(start_at, dest)]

    return bfs_internal(valves, start_at, dest)


# why not @memoize, because the ValveDict isn't hashable
@CallCounter
def bfs_internal(valves: ValveDict, start_at: str, dest: str) -> int:
    distances = {start_at: 0}
    queue = deque([start_at])
    visited: Set[str] = set()

    while True:
        visiting = queue.popleft()
        for edge in [e.name for e in valves[visiting].edges]:
            if edge == dest:
                bfs_cache[(start_at, dest)] = distances[visiting] + 1
                return distances[visiting] + 1
            if edge in visited:
                continue
            distances[edge] = distances[visiting] + 1
            queue.append(edge)


@CallCounter
def visit(
    valves: ValveDict,
    start_at: str,
    unvisited: Set[str],
    visited: Tuple[str, ...],
    current_score: int,
    flow_rate: int,
    this_day: int,
    days_spent: int,
    days_left: int,
) -> Tuple[int, Tuple[str, ...]]:

    this_valve = valves[start_at]

    # consume days
    current_score += flow_rate * days_spent
    days_left -= days_spent
    this_day += days_spent

    # print(
    #     f"Start of Day {this_day}: Visiting {start_at}, Unvisited = {unvisited}, visited = {visited}"
    # )

    # print(
    #     f"\tSpent {days_spent} days. With {days_left} days left,  released {flow_rate}*{days_spent}={flow_rate*days_spent} pressure. Total now {current_score}"
    # )

    # assert
    # expected_score = simulate_solution(valves, list(visited), this_day - 1)
    # if expected_score != current_score:
    #     print(f"Score {expected_score} from simulator but {current_score} in visit")
    #     print("Debugbreak")
    #     simulate_solution(valves, list(visited), this_day - 1, verbose=True)
    #     assert False

    # no more days
    if days_left == 0:
        # print(
        #     f"Start of Day {this_day}: Location {start_at}, Unvisited = {unvisited}, visited = {visited}"
        # )
        return (current_score, visited)

    # this move was illegal
    assert days_left >= 0

    # bump flow rate for future days
    # don't double dip when we backtrack
    if start_at in unvisited:
        flow_rate += this_valve.flow_rate
        unvisited_next = set(unvisited)
        unvisited_next.remove(start_at)
    else:
        unvisited_next = unvisited

    # track this move
    # visited_next = list(visited)
    # visited_next.append(start_at)
    # trombone_nasty
    if start_at != "AA":
        visited_next = visited + (start_at,)
    else:
        visited_next = visited

    # no more moves, consume all remaining time
    if len(unvisited_next) == 0:
        # if current_score + days_left * flow_rate == 1650:
        #     print("Break")

        # print(
        #     f"\t Final answer1: Spending last {days_left}, to release {flow_rate}*{days_left}={flow_rate*days_left} pressure. Total now {current_score + days_left * flow_rate}"
        # )

        # return (current_score + days_left * flow_rate, visited_next)
        return visit(
            valves=valves,
            start_at=start_at,
            unvisited=unvisited_next,
            visited=visited_next,
            current_score=current_score,
            flow_rate=flow_rate,
            this_day=this_day,
            days_spent=days_left,
            days_left=days_left,
        )

    # candidates = adjacent_candidates(valves, start_at, visited_next)
    candidates = unvisited_next

    costs = [
        # we pay one more day to open the valve
        bfs_shortest_distance(valves, start_at, candidate) + 1
        for candidate in candidates
    ]

    # print(
    #     f"From {start_at}, inspecting candidates {list(zip(candidates, costs))} from visited {visited_next} against threshold {days_left}"
    # )

    child_scores = [
        visit(
            valves=valves,
            start_at=candidate,
            unvisited=frozenset(unvisited_next),
            visited=tuple(visited_next),
            current_score=current_score,
            flow_rate=flow_rate,
            this_day=this_day,
            days_spent=cost,
            days_left=days_left,
        )
        for (candidate, cost) in zip(candidates, costs)
        if cost <= days_left
    ]

    # no valid moves
    if not child_scores:
        return visit(
            valves=valves,
            start_at=start_at,
            unvisited=unvisited_next,
            visited=visited_next,
            current_score=current_score,
            flow_rate=flow_rate,
            this_day=this_day,
            days_spent=days_left,
            days_left=days_left,
        )

        # return (current_score + days_left * flow_rate, visited_next)

    return max(child_scores, key=lambda answer: answer[0])


def part_one(lines, days_total=30) -> Tuple[int, List[str]]:
    CallCounter.clear()
    valves = parse_lines(lines)
    score = visit(
        valves,
        "AA",
        flow_rate=0,
        unvisited=frozenset([v.name for v in valves.values() if v.flow_rate != 0]),
        visited=("AA",),
        current_score=0,
        # it costs 0 days to enter the world
        this_day=0,
        days_spent=1,
        days_left=days_total + 1,
    )
    print(f"Function calls {CallCounter.counts()} times")
    # print(bfs_cache)
    return score


@CallCounter
def simulate_solution(
    valves: ValveDict, moves: List[str], minutes: int, verbose=False
) -> int:
    flow_rate = 0
    current_pressure = 0
    minute = 1
    visited: Set[str] = set()
    # ignore AA
    movelist = deque(moves)
    loc = movelist.popleft()

    def run_clock():
        nonlocal current_pressure
        nonlocal minute
        if verbose:
            print(f"== Minute {minute} ==")
        current_pressure += flow_rate
        if verbose:
            print(
                f"""Valves [{", ".join(sorted(list(visited)))}] are open, releasing {flow_rate} pressure. Total is now {current_pressure}""",
            )
        minute += 1

    while minute <= minutes:

        if len(movelist) > 0:
            dest = movelist.popleft()

            # greedy distance eval
            if verbose:
                remaining_time = 1 + minutes - minute
                candidates = set(
                    [v.name for v in valves.values() if v.flow_rate > 0]
                ).difference(visited)
                distances = [
                    bfs_shortest_distance(valves, loc, cand) for cand in candidates
                ]
                expected_values = [
                    valves[cand].flow_rate * (remaining_time - 1 - distances[idx])
                    for idx, cand in enumerate(candidates)
                ]
                print(f"Value map: {list(zip(candidates, distances, expected_values))}")
            #

            dist = bfs_shortest_distance(valves, loc, dest)
            for _ in range(dist):
                run_clock()
                if verbose:
                    print(f"Moving to {dest}")

            # consume another day to open the valve
            assert not dest in visited
            run_clock()
            if verbose:
                print(f"Opening {dest}")
            visited.add(dest)
            flow_rate += valves[dest].flow_rate
            loc = dest
        else:
            # run out the clock
            run_clock()
    return current_pressure


def part_two(lines) -> int:
    parse_lines(lines)
    return 0


def main() -> None:
    with open("day16_input.txt", "r") as file:
        lines = file.read().splitlines()
        # print_graph(parse_lines(lines))
        # import cProfile
        # import pstats

        # with cProfile.Profile() as pr:
        #     try:
        #         result = part_one(lines)
        #     finally:
        #         # pr.print_stats()
        #         stats = pstats.Stats(pr).sort_stats("cumtime")
        #         stats.print_stats()

        result = part_one(lines)
        print(result)
        # print(part_one(lines))
        # print(part_two(lines))


if __name__ == "__main__":
    main()
