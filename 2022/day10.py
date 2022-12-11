from typing import Any, Dict, List, TypeVar


def parse_lines(lines: List[str]) -> Any:
    return lines


def part_one(lines):
    input = parse_lines(lines)
    cycle = 0
    x_register = 1
    interesting_signals = []
    screen_x = 40
    pixels = []

    def clock():
        nonlocal cycle
        nonlocal pixels

        scan_pos = cycle % screen_x
        # clear the buffer
        if scan_pos == 0:
            pixels = ["."] * screen_x

        # render
        if abs(scan_pos - x_register) < 2:
            pixels[scan_pos] = "#"

        # end of line
        if scan_pos == screen_x - 1:
            print("".join(pixels))

        cycle += 1

        if cycle % screen_x == 20:
            # print(f"registering signal @ {cycle} = {cycle * x_register}")
            interesting_signals.append(cycle * x_register)

    for line in input:
        # process instruction
        if line == "noop":
            clock()
        elif line.startswith("addx"):
            param = int(line.split(" ")[1])
            clock()
            clock()
            x_register += param
        else:
            print(f"parse error [{line}]")
            assert False
        # check signal strengths
        # print(f"clock cycle = {cycle} x = {x_register}")

    return sum(interesting_signals)


def main():
    with open("day10_input.txt", "r") as file:
        lines = file.read().splitlines()
        print(part_one(lines))


if __name__ == "__main__":
    main()
