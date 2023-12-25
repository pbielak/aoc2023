"""Day 25"""
import networkx as nx


def parse_input(path: str) -> nx.Graph:
    with open(path, "r") as fin:
        g = nx.Graph()
        for line in fin.readlines():
            src, dsts = line.strip().split(": ")
            for dst in dsts.split(" "):
                g.add_edge(src, dst, capacity=1)

        return g


def solve_part_one(graph: nx.Graph) -> int:
    edges_to_remove = nx.minimum_edge_cut(graph)
    graph.remove_edges_from(edges_to_remove)

    answer = 1

    for cc in nx.connected_components(graph):
        answer *= len(cc)

    return answer


def run_tests():
    data = parse_input("data/example.txt")

    part_one = solve_part_one(data)
    print("Example - part 1:", part_one)
    assert part_one == 54

def main():
    run_tests()

    data = parse_input("data/input.txt")

    answer_one = solve_part_one(data)
    print("Part 1:", answer_one)


if __name__ == "__main__":
    main()

