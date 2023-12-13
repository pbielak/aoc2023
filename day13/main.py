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
    return compute_summary(data=data, accepted_diffs=0)


def solve_part_two(data: InputData) -> int:
    return compute_summary(data=data, accepted_diffs=1)


def compute_summary(data: InputData, accepted_diffs: int) -> int:
    summary = 0

    for pattern in data:
        v_idx = find_vertical_reflection_idx(pattern, accepted_diffs)
        h_idx = find_horizontal_reflection_idx(pattern, accepted_diffs)

        if v_idx is not None:
            summary += v_idx + 1

        if h_idx is not None:
            summary += 100 * (h_idx + 1)

    return summary


def find_horizontal_reflection_idx(
    pattern: Pattern,
    accepted_diffs: int,
) -> int | None:
    idxs = []

    for idx in range(len(pattern) - 1):
        rows_to_compare = [
            (idx - i, idx + i + 1)
            for i in range(idx + 1) 
            if idx - i >= 0 and idx + i + 1 < len(pattern)
        ]

        num_diffs = 0

        for i, j in rows_to_compare:
            num_diffs += compare_fn(pattern[i], pattern[j])

        if num_diffs == accepted_diffs:
            idxs.append(idx)

    if len(idxs) == 1:
        return idxs[0]
    elif len(idxs) == 0:
        return None
    else:
        raise RuntimeError(
            "Pattern should have at most one horizontal reflection"
        )


def find_vertical_reflection_idx(
    pattern: Pattern,
    accepted_diffs: int,
) -> int | None:
    idxs = []

    for idx in range(len(pattern[0]) - 1):
        cols_to_compare = [
            (idx - i, idx + i + 1)
            for i in range(idx + 1) 
            if idx - i >= 0 and idx + i + 1 < len(pattern[0])
        ]

        num_diffs = 0

        for i, j in cols_to_compare:
            num_diffs += compare_fn(
                first=[row[i] for row in pattern],
                second=[row[j] for row in pattern],
            )

        if num_diffs == accepted_diffs:
            idxs.append(idx)

    if len(idxs) == 1:
        return idxs[0]
    elif len(idxs) == 0:
        return None
    else:
        raise RuntimeError(
            "Pattern should have at most one vertical reflection"
        )


def compare_fn(first: str, second: str) -> int:
    """Returns the number of different characters between the inputs."""
    assert len(first) == len(second)
    diff = len(first)

    for a, b in zip(first, second):
        if a == b:
            diff -= 1

    return diff


def run_tests():
    data = parse_input("data/example.txt")

    part_one = solve_part_one(data)
    print("Example - part 1:", part_one)
    assert part_one == 405

    part_two = solve_part_two(data)
    print("Example - part 2:", part_two)
    assert part_two == 400


def main():
    run_tests()

    data = parse_input("data/input.txt")

    answer_one = solve_part_one(data)
    print("Part 1:", answer_one)

    answer_two = solve_part_two(data)
    print("Part 2:", answer_two)


if __name__ == "__main__":
    main()

