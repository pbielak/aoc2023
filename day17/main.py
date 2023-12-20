"""Day 17"""
import heapq


InputData = list[list[int]]


def parse_input(path: str) -> InputData:
    with open(path, "r") as fin:
        return [[int(d) for d in row.strip()] for row in fin.readlines()]


def solve_part_one(data: InputData) -> int:
    return find_shortest_path(
        start_point=(0, 0),
        end_point=(len(data) - 1, len(data[0]) - 1),
        heat_map=data,
        min_straight_steps=1,
        max_straight_steps=3,
    )


def solve_part_two(data: InputData) -> int:
    return find_shortest_path(
        start_point=(0, 0),
        end_point=(len(data) - 1, len(data[0]) - 1),
        heat_map=data,
        min_straight_steps=4,
        max_straight_steps=10,
    )


def find_shortest_path(
    start_point: tuple[int, int],
    end_point: tuple[int, int],
    heat_map: InputData,
    min_straight_steps: int,
    max_straight_steps: int,
) -> int:
    OFFSETS = {
        "VERTICAL": [(-1, 0), (1, 0)],
        "HORIZONTAL": [(0, -1), (0, 1)],
    }
    FLIP_DIRECTION = {"VERTICAL": "HORIZONTAL", "HORIZONTAL": "VERTICAL"}

    queue = [
        (0, (0, 0, "VERTICAL")),
        (0, (0, 0, "HORIZONTAL")),
    ]
    heapq.heapify(queue)
    visited = set()

    while queue:
        distance, (i, j, direction) = heapq.heappop(queue)

        if (i, j) == end_point:
            return distance

        if (i, j, direction) in visited:
            continue

        visited.add((i, j, direction))

        for di, dj in OFFSETS[direction]:
            new_distance = distance

            for num_steps in range(1, max_straight_steps + 1):
                new_i, new_j = i + di * num_steps, j + dj * num_steps

                if (
                    new_i < 0 or new_i >= len(heat_map)
                    or new_j < 0 or new_j >= len(heat_map[0])
                ):
                    break

                new_distance += heat_map[new_i][new_j]

                if (new_i, new_j, FLIP_DIRECTION[direction]) in visited:
                    continue

                if num_steps >= min_straight_steps:
                    heapq.heappush(
                        queue,
                        (
                            new_distance,
                            (new_i, new_j, FLIP_DIRECTION[direction]),
                        ),
                    )


def run_tests():
    data = parse_input("data/example.txt")

    part_one = solve_part_one(data)
    print("Example - part 1:", part_one)
    assert part_one == 102

    part_two = solve_part_two(data)
    print("Example - part 2:", part_two)
    assert part_two == 94


def main():
    run_tests()

    data = parse_input("data/input.txt")

    answer_one = solve_part_one(data)
    print("Part 1:", answer_one)

    answer_two = solve_part_two(data)
    print("Part 2:", answer_two)


if __name__ == "__main__":
    main()

