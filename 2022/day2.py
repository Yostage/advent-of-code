# https://adventofcode.com/2022/day/2
from enum import UNIQUE, Enum, verify

# The winner of the whole tournament is the player with the highest score.
# Your total score is the sum of your scores for each round.
# The score for a single round is the score for the shape you selected (1 for Rock, 2 for Paper, and 3 for Scissors)
# plus the score for the outcome of the round (0 if you lost, 3 if the round was a draw, and 6 if you won).


# the value is also the score
@verify(UNIQUE)
class RPS(Enum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3

    def rotate_down(self):
        if self.value == 1:
            return RPS(3)
        else:
            return RPS(self.value - 1)

    def rotate_up(self):
        if self.value == 3:
            return RPS(1)
        else:
            return RPS(self.value + 1)


def scoring(mine: RPS, theirs: RPS) -> int:
    # print(f"Decoding {mine} vs {theirs} as")
    # print(f"{mine.value} vs {theirs.value}")
    match mine.value - theirs.value:
        case 0:
            # draw
            return 3
        case 1 | -2:
            # win
            return 6
        case 2 | -1:
            # loss
            return 0
        case _:
            assert False


decoderRing = {
    "A": RPS.ROCK,
    "B": RPS.PAPER,
    "C": RPS.SCISSORS,
    "X": RPS.ROCK,
    "Y": RPS.PAPER,
    "Z": RPS.SCISSORS,
}


def calculate_move(desired_string: str, theirs: RPS) -> RPS:
    # good old rock nothing beats rock
    match desired_string:
        # lose
        case "X":
            return theirs.rotate_down()
        case "Y":
            return theirs
        case "Z":
            return theirs.rotate_up()
        case _:
            assert False


def sum_score_v1(lines):
    sum = 0
    for line in lines:
        [theirs_encoded, mine_encoded] = line.split(" ")
        theirs = RPS(decoderRing[theirs_encoded])
        mine = RPS(decoderRing[mine_encoded])
        # print(f"line [{line}]: {theirs} vs {mine} => {scoring(mine, theirs)}")
        sum += scoring(mine, theirs)
        sum += mine.value

    return sum


def sum_score_v2(lines):
    sum = 0
    for line in lines:
        [theirs_encoded, mine_encoded] = line.split(" ")
        theirs = RPS(decoderRing[theirs_encoded])
        mine = calculate_move(mine_encoded, theirs)
        # print(f"line [{line}]: {theirs} vs {mine} => {scoring(mine, theirs)}")
        sum += scoring(mine, theirs)
        sum += mine.value

    return sum


def main():
    with open("day2_input.txt", "r") as file:
        lines = [line.strip() for line in file]
    print(sum_score_v2(lines))


if __name__ == "__main__":
    main()
