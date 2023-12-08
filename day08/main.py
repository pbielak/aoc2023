"""Day 8"""
import math
import re
from itertools import cycle
from typing import NamedTuple


class Node(NamedTuple):
    name: str
    left_node: str
    right_node: str


class InputData(NamedTuple):
    instructions: list[str]
    nodes: dict[str, Node]


def parse_input(path: str) -> InputData:
    with open(path, "r") as fin:
        instructions = list(fin.readline().strip())

        fin.readline()

        nodes = {}
        for line in fin.readlines():
            parsed = re.search(
                pattern=(
                    "(?P<source>[A-Z1-9]{3}) = \("
                    "(?P<left>[A-Z1-9]{3}), "
                    "(?P<right>[A-Z1-9]{3})\)\n"
                ),
                string=line,
            )

            source = parsed.group("source")
            left = parsed.group("left")
            right = parsed.group("right")

            nodes[source] = Node(name=source, left_node=left, right_node=right)

        return InputData(instructions=instructions, nodes=nodes)


def solve_part_one(data: InputData) -> int:
    return get_path_length(data=data, node="AAA", stop_node="ZZZ")


def get_path_length(data: InputData, node: str, stop_node: str) -> int:
    path_length = 0

    current_node = node

    for instruction in cycle(data.instructions):
        if current_node.endswith(stop_node):
            break

        if instruction == "L":
            current_node = data.nodes[current_node].left_node
        else:
            current_node = data.nodes[current_node].right_node

        path_length += 1

    return path_length


def solve_part_two(data: InputData) -> int:
    start_nodes = [node for node in data.nodes.keys() if node.endswith("A")]
    path_lengths = [
        get_path_length(data=data, node=node, stop_node="Z")
        for node in start_nodes
    ]
    answer = math.lcm(*path_lengths)

    return answer


def run_tests():
    data = parse_input("data/example.txt")

    part_one = solve_part_one(data)
    print("Example - part 1:", part_one)
    assert part_one == 2

    data = parse_input("data/example2.txt")

    part_one = solve_part_one(data)
    print("Example2 - part 1:", part_one)
    assert part_one == 6

    data = parse_input("data/example3.txt")

    part_two = solve_part_two(data)
    print("Example3 - part 2:", part_two)
    assert part_two == 6

def main():
    run_tests()

    data = parse_input("data/input.txt")

    answer_one = solve_part_one(data)
    print("Part 1:", answer_one)

    answer_two = solve_part_two(data)
    print("Part 2:", answer_two)


if __name__ == "__main__":
    main()

