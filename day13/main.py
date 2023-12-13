"""Day 13"""
from typing import NamedTuple


Pattern = list[str]
InputData = list[Pattern]


def parse_input(path: str) -> InputData:
    with open(path, "r") as fin:
        data = []
        for pattern_raw in fin.read().split("\n\n"):
            data.append(pattern_raw.strip().split("\n"))

        return data


def solve_part_one(data: InputData) -> int:
    answer = 0

    for pattern in data:
        v_idx = find_vertical_reflection_idx(pattern)
        h_idx = find_horizontal_reflection_idx(pattern)

        if v_idx is not None:
            answer += v_idx + 1

        if h_idx is not None:
            answer += 100 * (h_idx + 1)

    return answer


def find_horizontal_reflection_idx(pattern: Pattern) -> int | None:
    idxs = []

    for idx in range(len(pattern) - 1):
        rows_to_compare = [
            (idx - i, idx + i + 1)
            for i in range(idx + 1) 
            if idx - i >= 0 and idx + i + 1 < len(pattern)
        ]
        if all(pattern[i] == pattern[j] for i, j in rows_to_compare):
            idxs.append(idx)

    if len(idxs) == 1:
        return idxs[0]
    elif len(idxs) == 0:
        return None
    else:
        raise RuntimeError(
            "Pattern should have at most one horizontal reflection"
        )


def find_vertical_reflection_idx(pattern: Pattern) -> int | None:
    idxs = []

    for idx in range(len(pattern[0]) - 1):
        cols_to_compare = [
            (idx - i, idx + i + 1)
            for i in range(idx + 1) 
            if idx - i >= 0 and idx + i + 1 < len(pattern[0])
        ]
        if all(row[i] == row[j] for i, j in cols_to_compare for row in pattern):
            idxs.append(idx)

    if len(idxs) == 1:
        return idxs[0]
    elif len(idxs) == 0:
        return None
    else:
        raise RuntimeError(
            "Pattern should have at most one vertical reflection"
        )

def solve_part_two(data: InputData) -> int:
    answer = ...

    return answer


def run_tests():
    data = parse_input("data/example.txt")

    part_one = solve_part_one(data)
    print("Example - part 1:", part_one)
    assert part_one == 405

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

