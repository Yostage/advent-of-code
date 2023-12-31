from dataclasses import dataclass
from functools import lru_cache
from typing import Dict, List


def parse_lines(lines: List[str]) -> List[str]:
    return lines[0].split(",")


@lru_cache
def hash_1(token: str) -> int:
    acc = 0
    for c in token:
        acc += ord(c)
        acc *= 17
        acc %= 256
    return acc


def part_one(lines) -> int:
    tokens = parse_lines(lines)
    return sum(hash_1(token) for token in tokens)


@dataclass
class Lens:
    label: str
    focus: int

    def __str__(self) -> str:
        return f"[{self.label} {self.focus}]"


def part_two(lines) -> int:
    def render(lens_list: Dict[int, List[Lens]]) -> None:
        print()
        for k, v in lens_list.items():
            if len(v) == 0:
                continue
            printed_list = " ".join(str(lens) for lens in v)
            print(f"Box {k}: {printed_list}")
        print()

    def pop_lens(lens_list: List[Lens], label: str) -> None:
        idx = next((i for i, v in enumerate(lens_list) if v.label == label), None)
        if idx is None:
            return
        del lens_list[idx]

    def insert_lens(lens_list: List[Lens], new_lens: Lens) -> None:
        idx = next(
            (i for i, v in enumerate(lens_list) if v.label == new_lens.label), None
        )
        if idx is not None:
            lens_list[idx] = new_lens
        else:
            lens_list.append(new_lens)

    hashmap: Dict[int, List[Lens]] = {i: [] for i in range(256)}
    tokens = parse_lines(lines)
    for token in tokens:
        if token[-1] == "-":
            label = token[:-1]
            pop_lens(hashmap[hash_1(label)], label)
        else:
            (label, focus) = token.split("=")
            insert_lens(hashmap[hash_1(label)], Lens(label=label, focus=int(focus)))
        # render(hashmap)

    return sum(
        (box + 1) * (slot + 1) * lens.focus
        for box, lenses in hashmap.items()
        for slot, lens in enumerate(lenses)
    )


def main() -> None:
    with open("day15_input.txt", "r") as file:
        lines = file.read().splitlines()
        print(part_one(lines))
        print(part_two(lines))


if __name__ == "__main__":
    main()
