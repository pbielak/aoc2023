"""Day 23"""

InputData = list[list[str]]
Position = tuple[int, int]
UP, DOWN = (-1, 0), (1, 0)
LEFT, RIGHT = (0, -1), (0, 1)


def parse_input(path: str) -> InputData:
    with open(path, "r") as fin:
        return [list(row.strip()) for row in fin.readlines()]


def solve_part_one(grid: InputData) -> int:
    start_point = (0, grid[0].index("."))
    end_point = (len(grid) - 1, grid[-1].index("."))

    edges = build_graph(grid)

    answer = find_longest_path(
        edges=edges,
        start_point=start_point,
        end_point=end_point,
    )

    return answer


def solve_part_two(data: InputData) -> int:
    dry_grid = [
        ["." if c in "^v<>" else c for c in row]
        for row in data
    ]
    answer = solve_part_one(dry_grid)

    return answer


def build_graph(grid: InputData) -> dict[Position, list[tuple[Position, int]]]:
    nodes = [
        (0, grid[0].index(".")),  # Start point
        (len(grid) - 1, grid[-1].index(".")),  # End point
        *get_junction_points(grid),
    ]
    edges = {node: [] for node in nodes} 

    for i, j in nodes:
        for _, direction in get_neighbors((i, j), grid, set()):
            end_i, end_j = i + direction[0], j + direction[1]
            path = [(i, j), (end_i, end_j)]

            while True:
                neighbors = get_neighbors((end_i, end_j), grid, set(path))
                
                if len(neighbors) == 0:
                    break
                elif len(neighbors) == 1:
                    path.append(neighbors[0][0])
                    end_i, end_j = neighbors[0][0]

                    if (end_i, end_j) in nodes:
                        break
                else:
                    assert (end_i, end_j) in nodes
                    break

            if path[-1] in nodes:
                edges[(i, j)].append((path[-1], len(path) - 1))

    return edges


def get_junction_points(grid: InputData) -> list[Position]:
    height = len(grid)
    width = len(grid[0])

    junction_points = []

    for i in range(height):
        for j in range(width):
            if grid[i][j] == ".":
                neighbors = []

                for di, dj in (UP, DOWN, LEFT, RIGHT):
                    new_i, new_j = i + di, j + dj

                    # New coordinates are valid?
                    if (
                        new_i < 0 or new_i >= height
                        or new_j < 0 or new_j >= width
                    ):
                        continue

                    # Is there forest?
                    if grid[new_i][new_j] == "#":
                        continue

                    neighbors.append((new_i, new_j))

                if len(neighbors) >= 3:
                    junction_points.append((i, j))

    return junction_points


def get_neighbors(
    point: Position,
    grid: InputData,
    visited: set[Position],
) -> list[Position]:
    height = len(grid)
    width = len(grid[0])

    neighbors = []

    for di, dj in (UP, DOWN, LEFT, RIGHT):
        new_i, new_j = point[0] + di, point[1] + dj

        # New coordinates are valid?
        if new_i < 0 or new_i >= height or new_j < 0 or new_j >= width:
            continue

        # Is there forest?
        if grid[new_i][new_j] == "#":
            continue

        # Are we moving downhill?
        if grid[new_i][new_j] == "^" and (di, dj) != UP:
            continue

        if grid[new_i][new_j] == "v" and (di, dj) != DOWN:
            continue

        if grid[new_i][new_j] == "<" and (di, dj) != LEFT:
            continue

        if grid[new_i][new_j] == ">" and (di, dj) != RIGHT:
            continue

        if (new_i, new_j) in visited:
            continue

        neighbors.append(((new_i, new_j), (di, dj)))

    return neighbors


def find_longest_path(
    edges: dict[Position, list[tuple[Position, int]]],
    start_point: Position,
    end_point: Position,
) -> int:
    def _f(node: Position, visited: set[Position], distance: int):
        if node == end_point:
            return distance

        dists = []

        for neighbor, weight in edges[node]:
            if neighbor in visited:
                continue

            dists.append(_f(neighbor, {*visited, neighbor}, distance + weight))

        return max([*dists, 0])

    return _f(start_point, {start_point}, 0)


def run_tests():
    data = parse_input("data/example.txt")

    part_one = solve_part_one(data)
    print("Example - part 1:", part_one)
    assert part_one == 94

    part_two = solve_part_two(data)
    print("Example - part 2:", part_two)
    assert part_two == 154


def main():
    run_tests()

    data = parse_input("data/input.txt")

    answer_one = solve_part_one(data)
    print("Part 1:", answer_one)

    answer_two = solve_part_two(data)
    print("Part 2:", answer_two)


if __name__ == "__main__":
    main()

