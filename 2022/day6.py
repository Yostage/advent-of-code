def find_signal(line: str, unique_len=4):
    # base case
    chars = list(line)
    buffer = chars[0:unique_len]
    marker = unique_len
    del chars[0:unique_len]
    for c in chars:
        if len(set(buffer)) == unique_len:
            return marker
        del buffer[0]
        buffer += c
        marker += 1

    assert False


def main():
    with open("day6_input.txt", "r") as file:
        lines = file.read().splitlines()

    # part one
    print(find_signal(lines[0]))
    # part two
    print(find_signal(lines[0], 14))


if __name__ == "__main__":
    main()
