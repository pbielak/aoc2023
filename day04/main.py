"""Day 4"""
from typing import NamedTuple


class Card(NamedTuple):
    ID: int
    winning_numbers: list[int]
    card_numbers: list[int]


    @classmethod
    def from_raw_str(cls, raw: str) -> "Card":
        card_info, numbers = raw.split(": ")

        card_id = int(card_info.replace("Card ", ""))

        winning_raw, card_raw = numbers.strip().replace("  ", " ").split(" | ")
        winning_numbers = [int(n) for n in winning_raw.split(" ")]
        card_numbers = [int(n) for n in card_raw.split(" ")]

        return cls(
            ID=card_id,
            winning_numbers=winning_numbers,
            card_numbers=card_numbers,
        )

    def n_matching_nums(self) -> int:
        intersecting_nums = (
            set(self.winning_numbers)
            .intersection(set(self.card_numbers))
        )

        return len(intersecting_nums)


InputData = list[Card]


def parse_input(path: str) -> InputData:
    with open(path, "r") as fin:
        return [
            Card.from_raw_str(line.strip())
            for line in fin.readlines()
        ]


def solve_part_one(data: InputData) -> int:
    answer = 0

    for card in data:
        n_matching_nums = card.n_matching_nums()

        if n_matching_nums > 0:
            points = 2 ** (n_matching_nums - 1)
        else:
            points = 0

        answer += points

    return answer


def solve_part_two(data: InputData) -> int:
    copies = [1] * len(data)

    for card in data:
        card_id = card.ID
        n_matching_nums = card.n_matching_nums()

        for off in range(n_matching_nums):
            copies[card_id + off] += copies[card_id - 1]

    answer = sum(copies)

    return answer


def run_tests():
    data = parse_input("data/example.txt")

    part_one = solve_part_one(data)
    print("Example - part 1:", part_one)
    assert part_one == 13

    part_two = solve_part_two(data)
    print("Example - part 2:", part_two)
    assert part_two == 30


def main():
    run_tests()

    data = parse_input("data/input.txt")

    answer_one = solve_part_one(data)
    print("Part 1:", answer_one)

    answer_two = solve_part_two(data)
    print("Part 2:", answer_two)


if __name__ == "__main__":
    main()

