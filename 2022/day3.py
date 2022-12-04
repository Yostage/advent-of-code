import itertools
from typing import Iterator, List


def char_to_priority(c: str) -> int:
    # Lowercase item types a through z have priorities 1 through 26.
    # Uppercase item types A through Z have priorities 27 through 52.
    assert len(c) == 1
    if c.islower():
        return 1 + ord(c[0]) - ord("a")
    elif c.isupper():
        return 27 + ord(c[0]) - ord("A")
    else:
        assert False


def find_shared_badge(compartment_strings: List[str]):
    assert len(compartment_strings) == 3
    badge = (
        set(compartment_strings[0])
        & set(compartment_strings[1])
        & set(compartment_strings[2])
    )
    assert len(badge) == 1
    return char_to_priority(list(badge)[0])


def find_shared_priority(compartment_string: str):
    # The list of items for each rucksack is given as characters all on a single line.
    # A given rucksack always has the same number of items in each of its two compartments,
    # so the first half of the characters represent items in the first compartment,
    # while the second half of the characters represent items in the second compartment.

    # split it in half
    # there must be exactly one character in the union
    # look it up in the priority table
    assert len(compartment_string) % 2 == 0
    mid = len(compartment_string) // 2
    left = compartment_string[:mid]
    right = compartment_string[mid:]
    shared_elements = list(set(left) & set(right))
    assert len(shared_elements) == 1
    return char_to_priority(shared_elements[0])


def grouper(iterator: Iterator, n: int) -> Iterator[list]:
    while chunk := list(itertools.islice(iterator, n)):
        yield chunk


def main():
    sum = 0
    with open("day3_input.txt", "r") as file:
        for chunk in grouper(iter(file.read().splitlines()), 3):
            sum += find_shared_badge(chunk)
    print(sum)


if __name__ == "__main__":
    main()
