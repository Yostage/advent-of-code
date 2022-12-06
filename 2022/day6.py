def find_signal(line: str):
    # base case
    chars = list(line)
    buffer = chars[0:4]
    marker = 4
    del chars[0:4]
    for c in chars:
        if len(set(buffer)) == 4:
            return marker
        del buffer[0]
        buffer += c
        marker += 1

    assert False


def main():
    with open("day6_input.txt", "r") as file:
        lines = file.read().splitlines()

    print(find_signal(lines[0]))


if __name__ == "__main__":
    main()
