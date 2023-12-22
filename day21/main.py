"""Day 21"""

InputData = list[list[str]]
Position = tuple[int, int]


def parse_input(path: str) -> InputData:
    with open(path, "r") as fin:
        return [list(line.strip()) for line in fin.readlines()]


def solve_part_one(data: InputData) -> int:
    return num_reachable_in_max_steps(grid=data, max_steps=64)


def num_reachable_in_max_steps(grid: InputData, max_steps: int) -> int:
    distances = traverse(grid=grid, max_steps=max_steps)
    num_reachable = sum(
        1 if d == max_steps or d % 2 == max_steps % 2 else 0 
        for d in distances.values()
    )
    return num_reachable


def traverse(
    grid: InputData,
    max_steps: int,
) -> dict[Position, int]:
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

        if distance == max_steps:
            continue

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

            if (new_i, new_j) in visited:
                continue

            queue.append(((new_i, new_j), distance + 1))

    return distances


def solve_part_two(data: InputData) -> int:
    answer = ...

    return answer


def run_tests():
    data = parse_input("data/example.txt")

    part_one = num_reachable_in_max_steps(grid=data, max_steps=6)
    print("Example - part 1:", part_one)
    assert part_one == 16

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

