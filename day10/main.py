"""Day 10"""
from typing import NamedTuple


class Position(NamedTuple):
    x: int
    y: int

    def north(self) -> "Position":
        return Position(self.x, self.y - 1)

    def south(self) -> "Position":
        return Position(self.x, self.y + 1)

    def west(self) -> "Position":
        return Position(self.x - 1, self.y)

    def east(self) -> "Position":
        return Position(self.x + 1, self.y)


class InputData(NamedTuple):
    start_pos: Position
    pipes: dict[Position, str]
    edges: dict[Position, tuple[Position, Position]]


def parse_input(path: str) -> InputData:
    with open(path, "r") as fin:
        pipes = {}
        start_pos = None

        for y, line in enumerate(fin.readlines()):
            for x, pipe in enumerate(line.strip()):
                if pipe == ".":
                    continue

                pos = Position(x, y)

                pipes[pos] = pipe

                if pipe == "S":
                    start_pos = pos

        # Get neighbors
        edges = {}

        for pos, pipe in pipes.items():
            neighbors = []
        
            if (
                pipe in ("S", "|", "L", "J") 
                and pipes.get(pos.north()) in ("|", "7", "F")
            ):
                neighbors.append(pos.north())

            if (
                pipe in ("S", "|", "7", "F")
                and pipes.get(pos.south()) in ("|", "L", "J")
            ):
                neighbors.append(pos.south())

            if (
                pipe in ("S", "-", "J", "7")
                and pipes.get(pos.west()) in ("-", "L", "F")
            ):
                neighbors.append(pos.west())

            if (
                pipe in ("S", "-", "L", "F")
                and pipes.get(pos.east()) in ("-", "J", "7")
            ):
                neighbors.append(pos.east())

            assert len(neighbors) <= 2, f"{pos} has {len(neighbors)} neighbors"
            edges[pos] = neighbors

        return InputData(start_pos=start_pos, pipes=pipes, edges=edges)


def solve_part_one(data: InputData) -> int:
    answer = find_loop_radius(data)

    return answer


def find_loop_radius(data: InputData) -> int:
    dists: dict[Position, int] = {}
    visited: set[Position] = set()

    queue = [(data.start_pos, 0)]

    while queue:
        pos, dist = queue.pop(0)

        if pos in visited:
            continue

        visited.add(pos)
        dists[pos] = dist

        for n_pos in data.edges.get(pos, []):
            queue.append((n_pos, dist + 1))

    return max(dists.values())



def solve_part_two(data: InputData) -> int:
    answer = ...

    return answer


def run_tests():
    data = parse_input("data/example.txt")

    part_one = solve_part_one(data)
    print("Example - part 1:", part_one)
    assert part_one == 8

    part_two = solve_part_two(data)
    print("Example - part 2:", part_two)
    assert part_two == ...

    data = parse_input("data/example2.txt")

    part_one = solve_part_one(data)
    print("Example2 - part 1:", part_one)
    assert part_one == 4


def main():
    run_tests()

    data = parse_input("data/input.txt")

    answer_one = solve_part_one(data)
    print("Part 1:", answer_one)

    answer_two = solve_part_two(data)
    print("Part 2:", answer_two)


if __name__ == "__main__":
    main()

