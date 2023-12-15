"""Day 5"""
from typing import NamedTuple


class RangeSpecifier(NamedTuple):
    dst_begin: int
    src_begin: int
    length: int


class Range(NamedTuple):
    mappings: list[RangeSpecifier]

    @classmethod
    def from_raw(cls, mappings: list[str]) -> "Range":
        return Range([
            RangeSpecifier(*[int(v) for v in mapping.split(" ")])
            for mapping in mappings
        ])

    def convert(self, value: int) -> int:
        for m in self.mappings:
            if m.src_begin <= value <= m.src_begin + m.length:
                return m.dst_begin + (value - m.src_begin)

        return value


class InputData(NamedTuple):
    seeds: list[int]
    maps: dict[tuple[str, str], Range]


def parse_input(path: str) -> InputData:
    with open(path, "r") as fin:
        seeds = [
            int(seed)
            for seed in fin.readline().strip().replace("seeds: ", "").split(" ")
        ]
        fin.readline()

        maps = {}
        for block in fin.read().split("\n\n"):
            name_raw, *mappings_raw = block.strip().split("\n")
            src, dst = name_raw.replace(" map:", "").split("-to-")
            _range = Range.from_raw(mappings_raw)

            maps[(src, dst)] = _range

        return InputData(seeds=seeds, maps=maps)


def solve_part_one(data: InputData) -> int:
    locations = []
    for seed in data.seeds:
        location = find_closest_location(seed, maps=data.maps)
#        print(seed, location)
        locations.append(location)

    return min(locations)


def find_closest_location(seed: int, maps: dict[tuple[str, str], Range]) -> int:
    soil = maps[("seed", "soil")].convert(value=seed)
    fertilizer = maps[("soil", "fertilizer")].convert(value=soil)
    water = maps[("fertilizer", "water")].convert(value=fertilizer)
    light = maps[("water", "light")].convert(value=water)
    temperature = maps[("light", "temperature")].convert(value=light)
    humidity = maps[("temperature", "humidity")].convert(value=temperature)
    location = maps[("humidity", "location")].convert(value=humidity)

#    print(seed, soil, fertilizer, water, light, temperature, humidity, location)

    return location


def solve_part_two(data: InputData) -> int:
    answer = ...

    return answer


def run_tests():
    data = parse_input("data/example.txt")

    part_one = solve_part_one(data)
    print("Example - part 1:", part_one)
    assert part_one == 35

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

