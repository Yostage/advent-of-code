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


def main():
    with open("day3_input.txt", "r") as file:
        pri = [find_shared_priority(line.strip()) for line in file]
    print(sum(pri))


if __name__ == "__main__":
    main()
