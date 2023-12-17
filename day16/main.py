"""Day 16"""
from typing import NamedTuple


class Point2D(NamedTuple):
    x: int
    y: int


class Beam(NamedTuple):
    position: Point2D
    direction: Point2D


InputData = list[list[str]]


def parse_input(path: str) -> InputData:
    with open(path, "r") as fin:
        return [list(line.strip()) for line in fin.readlines()]


def solve_part_one(data: InputData) -> int:
    energies = trace_beam(grid=data)
    answer = sum([sum(1 if c > 0 else 0 for c in row) for row in energies])

    return answer


def trace_beam(grid: InputData):
    energies = [[0] * len(grid[0]) for _ in range(len(grid))]

    beams = [
        Beam(position=Point2D(0, 0), direction=Point2D(1, 0)),
    ]
    traced = set()

    while beams:
        (x, y), (dx, dy) = beams.pop(0)

        if x < 0 or x >= len(grid[0]) or y < 0 or y >= len(grid):
            continue

        #print(f"Current beam: ({x}, {y}) D=({dx}, {dy})")
        #breakpoint()

        if (x, y, dx, dy) in traced:
            continue

        traced.add((x, y, dx, dy))

        # Register beam's energy
        energies[y][x] += 1

        # Update beam
        if grid[y][x] == ".":
            pass
        elif grid[y][x] == "/":
            if dx == 1:  # Right-moving
                dx, dy = 0, -1
            elif dx == -1:  # Left-moving
                dx, dy = 0, 1
            else:
                if dy == -1:  # Up-moving
                    dx, dy = 1, 0
                elif dy == 1:  # Down-moving
                    dx, dy = -1, 0
        elif grid[y][x] == "\\":
            if dx == 1:  # Right-moving
                dx, dy = 0, 1
            elif dx == -1:  # Left-moving
                dx, dy = 0, -1
            else:
                if dy == -1:  # Up-moving
                    dx, dy = -1, 0
                elif dy == 1:  # Down-moving
                    dx, dy = 1, 0
        elif grid[y][x] == "|":
            if dx == 1 or dx == -1:
                beams.append(Beam(position=Point2D(x, y - 1), direction=Point2D(0, -1)))
                beams.append(Beam(position=Point2D(x, y + 1), direction=Point2D(0, 1)))
                continue
        elif grid[y][x] == "-":
            if dy == 1 or dy == -1:
                beams.append(Beam(position=Point2D(x - 1, y), direction=Point2D(-1, 0)))
                beams.append(Beam(position=Point2D(x + 1, y), direction=Point2D(1, 0)))
                continue
        else:
            raise ValueError(f"Unknown tile: '{grid[y][x]}'")

        beams.append(Beam(position=Point2D(x + dx, y + dy), direction=Point2D(dx, dy)))

    return energies
    #print('\n'.join(''.join(['.' if c == 0 else "#" for c in row]) for row in energies))


def solve_part_two(data: InputData) -> int:
    answer = ...

    return answer


def run_tests():
    data = parse_input("data/example.txt")

    part_one = solve_part_one(data)
    print("Example - part 1:", part_one)
    assert part_one == 46

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

