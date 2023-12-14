"""Day 14"""
from copy import deepcopy
from typing import NamedTuple


InputData = list[list[str]]


def parse_input(path: str) -> InputData:
    with open(path, "r") as fin:
        return [list(row.strip()) for row in fin.readlines()]


def solve_part_one(data: InputData) -> int:
    updated = tilt_north(data)
    return compute_north_support_load(updated)


def solve_part_two(data: InputData) -> int:
    max_iter = 1_000_000_000
    out = deepcopy(data)

    cache = {}
    i = 0

    while True:
        key = to_tuple(out)
        if key in cache:
            break
        
        out = make_full_cycle(out)
        cache[key] = (out, i)

        i += 1

    _, cycle_begin_idx = cache[key]
    cycle_length = i - cycle_begin_idx
    num_steps = (max_iter - i) % cycle_length

    for _ in range(num_steps):
        out, _ = cache[to_tuple(out)]

    total_support_load = compute_north_support_load(out)
    return total_support_load


def to_tuple(x: InputData) -> tuple[str]:
    return tuple(''.join(row) for row in x)


def make_full_cycle(data: InputData) -> InputData:
    out = tilt_north(data)
    out = tilt_west(out)
    out = tilt_south(out)
    out = tilt_east(out)
    return out


def tilt_north(data: InputData) -> InputData:
    out = deepcopy(data)

    for row_idx, row in enumerate(out[1:], start=1):
        for col_idx, c in enumerate(row):
            if c == "O":  # Find rolling rocks 
                i = row_idx
                while i >= 1 and out[i - 1][col_idx] == ".":  # Move them north
                    out[i - 1][col_idx] = "O"
                    out[i][col_idx] = "."

                    i -= 1
    return out


def tilt_west(data: InputData) -> InputData:
    out = deepcopy(data)

    for row_idx in range(len(out)):
        for col_idx in range(1, len(out[0])):
            if out[row_idx][col_idx] == "O":  # Find rolling rocks 
                i = col_idx
                while i >= 1 and out[row_idx][i - 1] == ".":  # Move them west
                    out[row_idx][i - 1] = "O"
                    out[row_idx][i] = "."

                    i -= 1
    return out


def tilt_south(data: InputData) -> InputData:
    return tilt_north(data[::-1])[::-1]


def tilt_east(data: InputData) -> InputData:
    out = tilt_west([row[::-1] for row in data])
    return [row[::-1] for row in out]


def compute_north_support_load(data: InputData) -> int:
    support_load = 0

    for row_idx, row in enumerate(data):
        row_load = (len(data) - row_idx) * row.count("O")
        support_load += row_load

    return support_load


def run_tests():
    data = parse_input("data/example.txt")

    part_one = solve_part_one(data)
    print("Example - part 1:", part_one)
    assert part_one == 136

    part_two = solve_part_two(data)
    print("Example - part 2:", part_two)
    assert part_two == 64


def main():
    run_tests()

    data = parse_input("data/input.txt")

    answer_one = solve_part_one(data)
    print("Part 1:", answer_one)

    answer_two = solve_part_two(data)
    print("Part 2:", answer_two)


if __name__ == "__main__":
    main()

