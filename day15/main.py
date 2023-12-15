"""Day 15"""

InputData = list[str]


def parse_input(path: str) -> InputData:
    with open(path, "r") as fin:
        return fin.read().strip().split(",")


def solve_part_one(data: InputData) -> int:
    answer = 0

    for instruction in data:
        answer += hash(instruction)

    return answer


def hash(string: str) -> int:
    current_value = 0

    for c in string:
        current_value += ord(c)
        current_value *= 17
        current_value %= 256

    return current_value


def solve_part_two(data: InputData) -> int:
    boxes = [[] for _ in range(256)]

    for instruction in data:
        label = get_label(instruction)
        box_id = hash(label)

        if "-" in instruction:
            # Remove lens with given label
            boxes[box_id] = [lens for lens in boxes[box_id] if lens[0] != label]
        elif "=" in instruction:
            focal_length = int(instruction.split("=")[1])
            # Check if lens with given label exists...
            idx = [idx for idx, lens in enumerate(boxes[box_id]) if lens[0] == label]
            if idx:
                # ...and replace it
                boxes[box_id][idx[0]] = (label, focal_length)
            else:
                # ...or add it to the box
                boxes[box_id].append((label, focal_length))

    focusing_power = 0

    for box_id, lenses in enumerate(boxes, start=1):
        for lens_slot, (_, focal_length) in enumerate(lenses, start=1):
            focusing_power += box_id * lens_slot * focal_length

    return focusing_power


def get_label(instruction: str) -> str:
    out = instruction.replace("-", "")
    out = out.split("=")[0]
    return out


def run_tests():
    data = parse_input("data/example.txt")

    part_one = solve_part_one(data)
    print("Example - part 1:", part_one)
    assert part_one == 1_320

    part_two = solve_part_two(data)
    print("Example - part 2:", part_two)
    assert part_two == 145


def main():
    run_tests()

    data = parse_input("data/input.txt")

    answer_one = solve_part_one(data)
    print("Part 1:", answer_one)

    answer_two = solve_part_two(data)
    print("Part 2:", answer_two)


if __name__ == "__main__":
    main()

