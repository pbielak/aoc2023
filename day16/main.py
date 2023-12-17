"""Day 16"""
from typing import NamedTuple


class Beam(NamedTuple):
    position: tuple[int, int]
    direction: tuple[int, int]


InputData = list[list[str]]


def parse_input(path: str) -> InputData:
    with open(path, "r") as fin:
        return [list(line.strip()) for line in fin.readlines()]


def solve_part_one(data: InputData) -> int:
    energies = trace_beam(
        grid=data,
        start_beam=Beam(position=(0, 0), direction=(1, 0))
    )
    answer = sum([sum(1 if c > 0 else 0 for c in row) for row in energies])

    return answer


def solve_part_two(data: InputData) -> int:
    start_beams = [
        # Top
        *[
            Beam(position=(x, 0), direction=(0, 1))
            for x in range(len(data[0]))
        ],
        # Bottom
        *[
            Beam(position=(x, len(data) - 1), direction=(0, -1))
            for x in range(len(data[0]))
        ],
        # Left
        *[
            Beam(position=(0, y), direction=(1, 0))
            for y in range(len(data))
        ],
        # Right
        *[
            Beam(position=(len(data[0]) - 1, y), direction=(-1, 0))
            for y in range(len(data))
        ],
    ]

    answer = 0

    for start_beam in start_beams:
        energies = trace_beam(grid=data, start_beam=start_beam)
        n_energized_tiles = sum([
            sum(1 if c > 0 else 0 for c in row)
            for row in energies
        ])

        answer = max(answer, n_energized_tiles)

    return answer


def trace_beam(grid: InputData, start_beam: Beam) -> list[list[int]]:
    energies = [[0] * len(grid[0]) for _ in range(len(grid))]

    beams = [start_beam]
    traced = set()

    while beams:
        (x, y), (dx, dy) = beams.pop(0)

        if x < 0 or x >= len(grid[0]) or y < 0 or y >= len(grid):
            continue

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
                beams.append(Beam(position=(x, y - 1), direction=(0, -1)))
                beams.append(Beam(position=(x, y + 1), direction=(0, 1)))
                continue
        elif grid[y][x] == "-":
            if dy == 1 or dy == -1:
                beams.append(Beam(position=(x - 1, y), direction=(-1, 0)))
                beams.append(Beam(position=(x + 1, y), direction=(1, 0)))
                continue
        else:
            raise ValueError(f"Unknown tile: '{grid[y][x]}'")

        beams.append(Beam(position=(x + dx, y + dy), direction=(dx, dy)))

    return energies


def run_tests():
    data = parse_input("data/example.txt")

    part_one = solve_part_one(data)
    print("Example - part 1:", part_one)
    assert part_one == 46

    part_two = solve_part_two(data)
    print("Example - part 2:", part_two)
    assert part_two == 51


def main():
    run_tests()

    data = parse_input("data/input.txt")

    answer_one = solve_part_one(data)
    print("Part 1:", answer_one)

    answer_two = solve_part_two(data)
    print("Part 2:", answer_two)


if __name__ == "__main__":
    main()

