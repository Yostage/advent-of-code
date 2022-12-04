import heapq

# https://adventofcode.com/2022/day/1

# split the list into individual elves
# sum the value of each elf
# take the top value

example = """1000
2000
3000

4000

5000
6000

7000
8000
9000

10000
"""

# split line into lines
# accumulate elves
# sum each elf
def main():
    elves = []
    accumulator = 0
    with open("day1_input.txt", "r") as file:
        for line in file:
            line = line.strip()
            if line:
                accumulator += int(line)
            else:
                elves.append(accumulator)
                accumulator = 0

    # final elf
    elves.append(accumulator)
    accumulator = 0

    print(f"Max elf: {max(elves)}")

    top_3 = heapq.nlargest(3, elves)
    print(f"Sum of top elves: {sum(top_3)}")


main()
