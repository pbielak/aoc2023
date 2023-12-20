"""Day 18"""
from typing import Literal, NamedTuple


class Instruction(NamedTuple):
    direction: Literal["U", "D", "L", "R"]
    num_steps: int
    color_code: str

    @classmethod
    def from_raw(cls, line: str) -> "Instruction":
        direction, num_steps, color_code = line.strip().split(" ")
        return cls(direction, int(num_steps), color_code[1:-1])


InputData = list[Instruction]


def parse_input(path: str) -> InputData:
    with open(path, "r") as fin:
        return [Instruction.from_raw(line) for line in fin.readlines()]


def solve_part_one(data: InputData) -> int:
    area = compute_shape_area(data)
    return area


def solve_part_two(data: InputData) -> int:
    instructions = decode_instructions(data)
    area = compute_shape_area(instructions)
    return area


def compute_shape_area(instructions: list[Instruction]) -> int:
    OFFSETS = {"U": (-1, 0), "D": (1, 0), "L": (0, -1), "R": (0, 1)} 

    # Generate points from instructions
    points = [(0, 0)]
    y, x = points[0]

    for instruction in instructions:
        dy, dx = OFFSETS[instruction.direction]

        y += instruction.num_steps * dy
        x += instruction.num_steps * dx

        points.append((y, x))

    # Compute inside area (trapezoid formula)
    inside_area = 0
    for idx in range(len(points) - 1):
        y_i, x_i = points[idx]
        y_i1, x_i1 = points[idx + 1]

        inside_area += (y_i + y_i1) * (x_i - x_i1)

    inside_area = inside_area // 2

    # Compute boundary length
    boundary = 0

    for idx in range(len(points) - 1):
        y_i, x_i = points[idx]
        y_i1, x_i1 = points[idx + 1]

        boundary += abs(y_i1 - y_i) + abs(x_i1 - x_i)

    # Compute shape area
    area = inside_area + boundary // 2 + 1

    return area


def decode_instructions(instructions: list[Instruction]) -> list[Instruction]:
    DIRECTIONS = ["R", "D", "L", "U"]

    decoded = []
    
    for instruction in instructions:
        direction = DIRECTIONS[int(instruction.color_code[-1])]
        num_steps = int(instruction.color_code[1:-1], base=16)

        decoded.append(Instruction(direction, num_steps, ""))

    return decoded


def run_tests():
    data = parse_input("data/example.txt")

    part_one = solve_part_one(data)
    print("Example - part 1:", part_one)
    assert part_one == 62

    part_two = solve_part_two(data)
    print("Example - part 2:", part_two)
    assert part_two == 952_408_144_115


def main():
    run_tests()

    data = parse_input("data/input.txt")

    answer_one = solve_part_one(data)
    print("Part 1:", answer_one)

    answer_two = solve_part_two(data)
    print("Part 2:", answer_two)


if __name__ == "__main__":
    main()

