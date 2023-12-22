"""Day 21"""

InputData = list[list[str]]
Position = tuple[int, int]


def parse_input(path: str) -> InputData:
    with open(path, "r") as fin:
        return [list(line.strip()) for line in fin.readlines()]


def solve_part_one(data: InputData, max_steps: int = 64) -> int:
    distances = traverse(grid=data)
    num_reachable = sum(
        1 if d <= max_steps and d % 2 == max_steps % 2 else 0 
        for d in distances.values()
    )
    return num_reachable


def traverse(grid: InputData) -> dict[Position, int]:
    start_pos = [
        (i, j)
        for i, row in enumerate(grid)
        for j, c in enumerate(row)
        if c == "S"
    ][0]

    queue = [(start_pos, 0)]
    distances = {}
    visited = set()

    while queue:
        pos, distance = queue.pop(0)

        if pos in visited:
            continue

        distances[pos] = distance
        visited.add(pos)

        for di, dj in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            i, j = pos
            new_i, new_j = i + di, j + dj

            if (
                new_i < 0 or new_i >= len(grid)
                or new_j < 0 or new_j >= len(grid[0])
            ):
                continue

            if grid[new_i][new_j] == "#":
                continue

            queue.append(((new_i, new_j), distance + 1))

    return distances


def solve_part_two(data: InputData, max_steps: int = 26_501_365) -> int:
    """https://github.com/villuna/aoc23/wiki/A-Geometric-solution-to-advent-of-code-2023,-day-21"""
    width = len(data[0])
    threshold = width // 2

    distances = traverse(grid=data)

    num_even_corners = len([
        d 
        for d in distances.values()
        if d % 2 == 0 and d > threshold
    ])
    num_odd_corners = len([
        d for d in distances.values()
        if d % 2 == 1 and d > threshold
    ])

    num_even_full = len([d for d in distances.values() if d % 2 == 0])
    num_odd_full = len([d for d in distances.values() if d % 2 == 1])

    n = (max_steps - (width // 2)) // width
    answer = (
        ((n + 1) * (n + 1)) * num_odd_full
        + (n*n) * num_even_full
        - (n+1) * num_odd_corners
        + n * num_even_corners
    )

    return answer


def run_tests():
    data = parse_input("data/example.txt")

    part_one = solve_part_one(data, max_steps=6)
    print("Example - part 1:", part_one)
    assert part_one == 16


def main():
    run_tests()

    data = parse_input("data/input.txt")

    answer_one = solve_part_one(data)
    print("Part 1:", answer_one)

    answer_two = solve_part_two(data)
    print("Part 2:", answer_two)


if __name__ == "__main__":
    main()

