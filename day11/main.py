"""Day 11"""
from itertools import combinations
from typing import NamedTuple


InputData = list[list[str]]


def parse_input(path: str) -> InputData:
    with open(path, "r") as fin:
        return [
            [c for c in line.strip()]
            for line in fin.readlines()
        ]


def solve_part_one(data: InputData) -> int:
    return sum(compute_shortest_distances(image=data, expansion_rate=2))


def solve_part_two(data: InputData, expansion_rate: int) -> int:
    dists_1 = compute_shortest_distances(image=data, expansion_rate=1)
    dists_2 = compute_shortest_distances(image=data, expansion_rate=2)

    scaled_sd = [
        d_1 + (d_2 - d_1) * (expansion_rate - 1)
        for d_1, d_2 in zip(dists_1, dists_2)
    ]

    return sum(scaled_sd)


def compute_shortest_distances(
    image: InputData,
    expansion_rate: int,
) -> list[int]:
    expanded_image = expand(image, expansion_rate)
    galaxy_positions = [
        (y, x)
        for y, row in enumerate(expanded_image)
        for x, pixel in enumerate(row)
        if pixel == "#"
    ]

    shortest_distances = []
    for (y1, x1), (y2, x2) in combinations(galaxy_positions, r=2):
        shortest_distances.append(abs(y1 - y2) + abs(x1 - x2))

    return shortest_distances


def expand(image: InputData, expansion_rate: int) -> InputData:
    out = []

    # Expand rows
    for row in image:
        out.append(row)

        if set(row) == {"."}:
            out.extend([row] * (expansion_rate - 1))

    # Expand columns
    x = 0
    while x < len(out[0]):
        if all(row[x] == "." for row in out):
            out = [
                [
                    *row[:x],
                    *["."] * (expansion_rate - 1),
                    *row[x:],
                ]
                for row in out
            ]
            x += expansion_rate - 1

        x += 1

    return out


def run_tests():
    data = parse_input("data/example.txt")

    part_one = solve_part_one(data)
    print("Example - part 1:", part_one)
    assert part_one == 374

    part_two_10 = solve_part_two(data, expansion_rate=10)
    print("Example - part 2 (x10):", part_two_10)
    assert part_two_10 == 1_030

    part_two_100 = solve_part_two(data, expansion_rate=100)
    print("Example - part 2 (x100):", part_two_100)
    assert part_two_100 == 8_410


def main():
    run_tests()

    data = parse_input("data/input.txt")

    answer_one = solve_part_one(data)
    print("Part 1:", answer_one)

    answer_two = solve_part_two(data, expansion_rate=1_000_000)
    print("Part 2:", answer_two)


if __name__ == "__main__":
    main()

