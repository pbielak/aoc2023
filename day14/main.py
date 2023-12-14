"""Day 14"""
from typing import NamedTuple


InputData = list[list[str]]


def parse_input(path: str) -> InputData:
    with open(path, "r") as fin:
        return [list(row.strip()) for row in fin.readlines()]


def solve_part_one(data: InputData) -> int:
    updated = tilt_north(data)
    answer = 0

    for row_idx, row in enumerate(updated):
        row_load = (len(updated) - row_idx) * row.count("O")
        answer += row_load

    return answer


def tilt_north(data: InputData) -> InputData:
    out = data.copy()

    for row_idx, row in enumerate(out[1:], start=1):
        for col_idx, c in enumerate(row):
            if c == "O":  # Find rolling rocks 
                i = row_idx
                while i >= 1 and out[i - 1][col_idx] == ".":  # Move them north
                    out[i - 1][col_idx] = "O"
                    out[i][col_idx] = "."

                    i -= 1
    return out


def solve_part_two(data: InputData) -> int:
    answer = ...

    return answer


def run_tests():
    data = parse_input("data/example.txt")

    part_one = solve_part_one(data)
    print("Example - part 1:", part_one)
    assert part_one == 136

    part_two = solve_part_two(data)
    print("Example - part 2:", part_two)
    assert part_two == ...


def main():
    run_tests()

    data = parse_input("data/input.txt")

    answer_one = solve_part_one(data)
    print("Part 1:", answer_one)

    answer_two = solve_part_two(data)
    print("Part 2:", answer_two)


if __name__ == "__main__":
    main()

