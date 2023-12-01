"""Day 1"""
SPELLED_TO_DIGIT = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}

T_Data = list[str]


def parse_input(path: str) -> T_Data:
    with open(path, "r") as fin:
        return [line.strip() for line in fin.readlines()]


def solve_part_one(data: T_Data) -> int:
    digits = [
        [c for c in line if c.isnumeric()]
        for line in data
    ]
    numbers = [int(d[0] + d[-1]) for d in digits]

    answer = sum(numbers)
    return answer


def get_digit_positions(line: str) -> list[int]:
    return [idx for idx, c in enumerate(line) if c.isnumeric()]


def find_first_spelled_digit(line: str) -> str:
    d_pos = get_digit_positions(line)

    if not d_pos:
        end = len(line)
    else:
        end = d_pos[0]

    i = 0
    while i <= end:
        for spelled, digit in SPELLED_TO_DIGIT.items():
            if spelled in line[:i]:
                return digit
        i += 1

    return line[d_pos[0]]


def find_last_spelled_digit(line: str) -> str:
    d_pos = get_digit_positions(line)

    if not d_pos:
        start = 0
    else:
        start = d_pos[-1]

    i = len(line) - 1
    while start <= i:
        for spelled, digit in SPELLED_TO_DIGIT.items():
            if spelled in line[i:]:
                return digit
        i -= 1

    return line[d_pos[-1]]


def solve_part_two(data: T_Data) -> int:
    numbers = []
    for line in data:
        f_digit = find_first_spelled_digit(line)
        l_digit = find_last_spelled_digit(line)

        numbers.append(int(f_digit + l_digit))

    answer = sum(numbers)
    return answer


def run_tests():
    data = parse_input("data/example.txt")
    part_one = solve_part_one(data)
    print("Example - part 1:", part_one)
    assert part_one == 142

    data = parse_input("data/example2.txt")
    part_two = solve_part_two(data)
    print("Example - part 2:", part_two)
    assert part_two == 281


def main():
    run_tests()

    data = parse_input("data/input.txt")

    answer_one = solve_part_one(data)
    print("Part 1:", answer_one)

    answer_two = solve_part_two(data)
    print("Part 2:", answer_two)


if __name__ == "__main__":
    main()

