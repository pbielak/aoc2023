"""Day 6"""
import re
from typing import NamedTuple


class RaceStats(NamedTuple):
    duration_ms: int
    best_distance_mm: int


InputData = list[RaceStats]


def parse_input(path: str) -> InputData:
    with open(path, "r") as fin:
        times = [int(t) for t in re.findall("\d+", fin.readline())]
        distances = [int(d) for d in re.findall("\d+", fin.readline())]

        return [
            RaceStats(duration_ms=time, best_distance_mm=distance)
            for time, distance in zip(times, distances)
        ]


def solve_part_one(data: InputData) -> int:
    answer = 1

    for race_stats in data:
        num_ways_win = 0
        for button_pressed_ms in range(1, race_stats.duration_ms + 1):
            distance_travelled_mm = (
                button_pressed_ms
                * (race_stats.duration_ms - button_pressed_ms)
            )

            if distance_travelled_mm > race_stats.best_distance_mm:
                num_ways_win += 1

        answer *= num_ways_win

    return answer


def solve_part_two(data: InputData) -> int:
    time, distance = "", ""
    for race_stats in data:
        time += str(race_stats.duration_ms)
        distance += str(race_stats.best_distance_mm)

    answer = solve_part_one([
        RaceStats(duration_ms=int(time), best_distance_mm=int(distance))
    ])

    return answer


def run_tests():
    data = parse_input("data/example.txt")

    part_one = solve_part_one(data)
    print("Example - part 1:", part_one)
    assert part_one == 288

    part_two = solve_part_two(data)
    print("Example - part 2:", part_two)
    assert part_two == 71_503


def main():
    run_tests()

    data = parse_input("data/input.txt")

    answer_one = solve_part_one(data)
    print("Part 1:", answer_one)

    answer_two = solve_part_two(data)
    print("Part 2:", answer_two)


if __name__ == "__main__":
    main()

