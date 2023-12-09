"""Day 9"""

InputData = list[list[int]]


def parse_input(path: str) -> InputData:
    with open(path, "r") as fin:
        return [
            [int(n) for n in line.strip().split(" ")]
            for line in fin.readlines()
        ]


def solve_part_one(data: InputData) -> int:
    answer = 0

    for seq in data:
        _, pred_right = extrapolate(seq)
        answer += pred_right

    return answer


def extrapolate(seq: list[int]) -> tuple[int, int]:
    diffs = [seq]

    while True:
        current_diff = [b - a for b, a in zip(diffs[-1][1:], diffs[-1][:-1])] 

        if all(n == 0 for n in current_diff):
            break
        
        diffs.append(current_diff)

    pred_left = 0
    pred_right = 0
    for diff in diffs[::-1]:
        pred_left = diff[0] - pred_left
        pred_right += diff[-1]

    return pred_left, pred_right


def solve_part_two(data: InputData) -> int:
    answer = 0

    for seq in data:
        pred_left, _ = extrapolate(seq)
        answer += pred_left

    return answer


def run_tests():
    data = parse_input("data/example.txt")

    part_one = solve_part_one(data)
    print("Example - part 1:", part_one)
    assert part_one == 114

    part_two = solve_part_two(data)
    print("Example - part 2:", part_two)
    assert part_two == 2


def main():
    run_tests()

    data = parse_input("data/input.txt")

    answer_one = solve_part_one(data)
    print("Part 1:", answer_one)

    answer_two = solve_part_two(data)
    print("Part 2:", answer_two)


if __name__ == "__main__":
    main()

