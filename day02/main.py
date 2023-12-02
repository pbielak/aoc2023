"""Day 2"""
from typing import NamedTuple


class CubesSample(NamedTuple):
    n_red: int
    n_green: int
    n_blue: int


class Game(NamedTuple):
    ID: int
    subsets: list[CubesSample]


T_Data = list[Game]


def parse_input(path: str) -> T_Data:
    data = []

    with open(path, "r") as fin:
        for line in fin.readlines():
            game_raw, subsets_raw = line.strip().split(": ")

            game_id = int(game_raw.replace("Game ", ""))

            subsets = []
            for subs in subsets_raw.split("; "):
                n_red, n_green, n_blue = 0, 0, 0

                for sub in subs.split(", "):
                    if "red" in sub:
                        n_red = int(sub.replace(" red", ""))
                    if "green" in sub:
                        n_green = int(sub.replace(" green", ""))
                    if "blue" in sub:
                        n_blue = int(sub.replace(" blue", ""))

                subsets.append(
                    CubesSample(
                        n_red=n_red,
                        n_green=n_green,
                        n_blue=n_blue,
                    )
                )

            data.append(Game(ID=game_id, subsets=subsets))

    return data


def solve_part_one(data: T_Data) -> int:
    max_n_red = 12
    max_n_green = 13
    max_n_blue = 14

    answer = 0

    for game in data:
        if all(
            sample.n_red <= max_n_red
            and sample.n_green <= max_n_green
            and sample.n_blue <= max_n_blue
            for sample in game.subsets
        ):
            answer += game.ID

    return answer


def solve_part_two(data: T_Data) -> int:
    answer = 0

    for game in data:
        min_n_red = 0
        min_n_green = 0
        min_n_blue = 0

        for sample in game.subsets:
            min_n_red = max(sample.n_red, min_n_red)
            min_n_green = max(sample.n_green, min_n_green)
            min_n_blue = max(sample.n_blue, min_n_blue)

        answer += min_n_red * min_n_green * min_n_blue

    return answer


def run_tests():
    data = parse_input("data/example.txt")

    part_one = solve_part_one(data)
    print("Example - part 1:", part_one)
    assert part_one == 8

    part_two = solve_part_two(data)
    print("Example - part 2:", part_two)
    assert part_two == 2_286


def main():
    run_tests()

    data = parse_input("data/input.txt")

    answer_one = solve_part_one(data)
    print("Part 1:", answer_one)

    answer_two = solve_part_two(data)
    print("Part 2:", answer_two)


if __name__ == "__main__":
    main()

