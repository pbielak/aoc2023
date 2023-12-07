"""Day 7"""
from collections import Counter
from enum import Enum
from typing import NamedTuple


class Hand(NamedTuple):
    cards: list[str]
    bid: int


class HandType(Enum):
    FIVE_OF_A_KIND = 7
    FOUR_OF_A_KIND = 6
    FULL_HOUSE = 5
    THREE_OF_A_KIND = 4
    TWO_PAIR = 3
    ONE_PAIR = 2
    HIGH_CARD = 1

    @classmethod
    def get_type(cls, cards: str) -> int:
        counts = [c for _, c in Counter(cards).most_common()]
        return cls._counts_to_type(counts=counts)

    @classmethod
    def get_type_with_joker(cls, cards: str) -> int:
        num_jokers = cards.count("J")
        counts = [
            cnt 
            for _, cnt in Counter([c for c in cards if c != "J"]).most_common()
        ]

        if not counts:
            counts = [5]  # All jokers
        else:
            counts[0] += num_jokers

        return cls._counts_to_type(counts=counts)

    @classmethod
    def _counts_to_type(cls, counts: list[int]) -> int:
        if counts == [5]:
            return cls.FIVE_OF_A_KIND.value
        elif counts == [4, 1]:
            return cls.FOUR_OF_A_KIND.value
        elif counts == [3, 2]:
            return cls.FULL_HOUSE.value
        elif counts == [3, 1, 1]:
            return cls.THREE_OF_A_KIND.value
        elif counts == [2, 2, 1]:
            return cls.TWO_PAIR.value
        elif counts == [2, 1, 1, 1]:
            return cls.ONE_PAIR.value
        else:
            return cls.HIGH_CARD.value


InputData = list[Hand]


def parse_input(path: str) -> InputData:
    with open(path, "r") as fin:
        data = []
        for line in fin.readlines():
            cards, bid = line.strip().split(" ")
            data.append(Hand(cards=list(cards), bid=int(bid)))

        return data


def solve_part_one(data: InputData) -> int:
    return compute_answer(
        data=data,
        type_fn=HandType.get_type,
        card_priorities=[
            "2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A",
        ],
    )


def solve_part_two(data: InputData) -> int:
    return compute_answer(
        data=data,
        type_fn=HandType.get_type_with_joker,
        card_priorities=[
            "J", "2", "3", "4", "5", "6", "7", "8", "9", "T", "Q", "K", "A",
        ],
    )


def compute_answer(
    data: InputData,
    type_fn,
    card_priorities: list[str],
) -> int:
    answer = 0

    sorted_hands = sorted(
        data,
        key=lambda hand: (
            type_fn(hand.cards),
            *[card_priorities.index(card) for card in hand.cards],
        ),
    )


    for rank, hand in zip(range(1, len(data) + 1), sorted_hands):
        answer += rank * hand.bid

    return answer


def run_tests():
    assert HandType.get_type("AAAAA") == 7
    assert HandType.get_type("AA8AA") == 6
    assert HandType.get_type("23332") == 5
    assert HandType.get_type("TTT98") == 4
    assert HandType.get_type("23432") == 3
    assert HandType.get_type("A23A4") == 2
    assert HandType.get_type("23456") == 1

    assert HandType.get_type_with_joker("32T3K") == 2  # ONE PAIR
    assert HandType.get_type_with_joker("KK677") == 3  # TWO PAIR
    assert HandType.get_type_with_joker("T55J5") == 6  # FOUR OF A KIND
    assert HandType.get_type_with_joker("KTJJT") == 6  # FOUR OF A KIND
    assert HandType.get_type_with_joker("QQQJA") == 6  # FOUR OF A KIND

    data = parse_input("data/example.txt")

    part_one = solve_part_one(data)
    print("Example - part 1:", part_one)
    assert part_one == 6_440

    part_two = solve_part_two(data)
    print("Example - part 2:", part_two)
    assert part_two == 5_905


def main():
    run_tests()

    data = parse_input("data/input.txt")

    answer_one = solve_part_one(data)
    print("Part 1:", answer_one)

    answer_two = solve_part_two(data)
    print("Part 2:", answer_two)


if __name__ == "__main__":
    main()

