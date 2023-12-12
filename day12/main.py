"""Day 12"""
from itertools import product
from typing import Generator, NamedTuple


class SpringInfo(NamedTuple):
    state: list[str]
    sizes: list[int]


InputData = list[SpringInfo]


def parse_input(path: str) -> InputData:
    with open(path, "r") as fin:
        data = []
        for line in fin.readlines():
            state_raw, sizes_raw = line.strip().split(" ")
            sizes = [int(s) for s in sizes_raw.split(",")]
            data.append(SpringInfo(state=list(state_raw), sizes=sizes))

        return data


def solve_part_one(data: InputData) -> int:
    answer = 0

    for spring_info in data:
        num_arrangements = 0
        for state in generate_arrangements(spring_info.state):
            if get_block_sizes(state) == spring_info.sizes:
                num_arrangements += 1

        answer += num_arrangements

    return answer


def generate_arrangements(state: list[str]) -> Generator[list[str], None, None]:
    unknown_pos = [i for i, c in enumerate(state) if c == "?"]

    for fields in product([".", "#"], repeat=len(unknown_pos)):
        current_state = state.copy()
        for pos, f in zip(unknown_pos, fields):
            current_state[pos] = f
        yield current_state


def get_block_sizes(state: list[str]) -> list[int]:
    block_sizes = []

    block = ""
    for i in range(len(state)):
        if state[i] == ".":
            if block:
                block_sizes.append(len(block))
                block = ""
        elif state[i] == "#":
            block += "#"

    if block:
        block_sizes.append(len(block))

    return block_sizes


def solve_part_two(data: InputData) -> int:
    answer = ...

    return answer


def run_tests():
    data = parse_input("data/example.txt")

    part_one = solve_part_one(data)
    print("Example - part 1:", part_one)
    assert part_one == 21

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

