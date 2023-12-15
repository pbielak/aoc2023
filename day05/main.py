"""Day 5"""
from typing import NamedTuple


class Range(NamedTuple):
    begin: int
    length: int

    @property
    def end(self) -> int:
        return self.begin + self.length - 1

    def contains(self, value: int) -> bool:
        return self.begin <= value <= self.end

    def contains_range(self, other: "Range") -> bool:
        return self.begin <= other.begin and other.end <= self.end

    def __repr__(self) -> str:
        return f"[{self.begin:_}...{self.end:_}]"


class Map(NamedTuple):
    mappings: list[tuple[Range, Range]]

    @classmethod
    def from_raw(cls, mappings: list[str]) -> "Range":
        _mappings = []
        for mapping in mappings:
            dst_begin, src_begin, length = [int(v) for v in mapping.split(" ")]
            _mappings.append(
                (Range(src_begin, length), Range(dst_begin, length))
            )
        _mappings = sorted(_mappings, key=lambda rs: rs[0].begin)
        return cls(_mappings)

    def convert(self, value: int) -> int:
        for src_range, dst_range in self.mappings:
            if src_range.contains(value):
                return dst_range.begin - src_range.begin + value

        return value

    def convert_range(self, r: Range) -> list[Range]:
        for src_range, dst_range in self.mappings:
            diff = dst_range.begin - src_range.begin

            if src_range.contains_range(r):
                out = Range(
                    begin=r.begin + diff,
                    length=r.length,
                )
                return [out]

            elif src_range.begin <= r.begin <= src_range.end:
                r1 = Range(
                    begin=r.begin + diff,
                    length=src_range.length - (r.begin - src_range.begin),
                )
                r2 = Range(
                    begin=src_range.end + 1,
                    length=r.end - src_range.end,
                )
                assert r1.length + r2.length == r.length

                return [r1, *self.convert_range(r2)]

            elif src_range.begin <= r.end <= src_range.end:
                r1 = Range(
                    begin=r.begin,
                    length=src_range.begin - r.begin,
                )
                r2 = Range(
                    begin=src_range.begin,
                    length=r.end - src_range.begin + 1,
                )
                assert r1.length + r2.length == r.length

                return [*self.convert_range(r1), r2]

        return [r]


class InputData(NamedTuple):
    seeds: list[int]
    maps: dict[tuple[str, str], Map]


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
            _map = Map.from_raw(mappings_raw)

            maps[(src, dst)] = _map

        return InputData(seeds=seeds, maps=maps)


def solve_part_one(data: InputData) -> int:
    locations = []
    for seed in data.seeds:
        location = find_closest_location(seed, maps=data.maps)
        locations.append(location)

    return min(locations)


def find_closest_location(seed: int, maps: dict[tuple[str, str], Map]) -> int:
    soil = maps[("seed", "soil")].convert(value=seed)
    fertilizer = maps[("soil", "fertilizer")].convert(value=soil)
    water = maps[("fertilizer", "water")].convert(value=fertilizer)
    light = maps[("water", "light")].convert(value=water)
    temperature = maps[("light", "temperature")].convert(value=light)
    humidity = maps[("temperature", "humidity")].convert(value=temperature)
    location = maps[("humidity", "location")].convert(value=humidity)

    return location


def solve_part_two(data: InputData) -> int:
    def _convert_all(input_ranges, key) -> list[Range]:
        return [
            r
            for ir in input_ranges
            for r in data.maps[key].convert_range(ir)
        ]


    seed_ranges = []
    for i in range(0, len(data.seeds) - 1, 2):
        src, length = data.seeds[i], data.seeds[i + 1]
        seed_ranges.append(Range(src, length))

    soil_ranges = _convert_all(seed_ranges, ("seed", "soil"))
    fertilizer_ranges = _convert_all(soil_ranges, ("soil", "fertilizer"))
    water_ranges = _convert_all(fertilizer_ranges, ("fertilizer", "water"))
    light_ranges = _convert_all(water_ranges, ("water", "light"))
    temp_ranges = _convert_all(light_ranges, ("light", "temperature"))
    humidity_ranges = _convert_all(temp_ranges, ("temperature", "humidity"))
    location_ranges = _convert_all(humidity_ranges, ("humidity", "location"))

    answer = min(lr.begin for lr in location_ranges)

    return answer


def run_tests():
    data = parse_input("data/example.txt")

    part_one = solve_part_one(data)
    print("Example - part 1:", part_one)
    assert part_one == 35

    part_two = solve_part_two(data)
    print("Example - part 2:", part_two)
    assert part_two == 46


def main():
    run_tests()

    data = parse_input("data/input.txt")

    answer_one = solve_part_one(data)
    print("Part 1:", answer_one)

    answer_two = solve_part_two(data)
    print("Part 2:", answer_two)


if __name__ == "__main__":
    main()

