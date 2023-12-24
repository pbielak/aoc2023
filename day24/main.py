"""Day 24"""
from itertools import combinations
from typing import NamedTuple


class Hailstone(NamedTuple):
    x: int
    y: int
    z: int
    vx: int
    vy: int
    vz: int

    @classmethod
    def from_raw(cls, raw: str) -> "Hailstone":
        pos, vel = raw.strip().split(" @ ")
        x, y, z = [int(p) for p in pos.split(", ")]
        vx, vy, vz = [int(v) for v in vel.split(", ")]
        return cls(x, y, z, vx, vy, vz)


InputData = list[Hailstone]


def parse_input(path: str) -> InputData:
    with open(path, "r") as fin:
        return [Hailstone.from_raw(line) for line in fin.readlines()]


def solve_part_one(data: InputData, val_min: int, val_max: int) -> int:
    answer = 0

    for h1, h2 in combinations(data, r=2):
        res = intersection_point_2d(h1, h2)
        if res is not None:
            x, y = res
            if val_min <= x <= val_max and val_min <= y <= val_max:
                answer += 1

    return answer


def intersection_point_2d(
    h1: Hailstone,
    h2: Hailstone,
) -> tuple[float, float] | None:
    denom = h2.vx * h1.vy - h1.vx * h2.vy

    if denom == 0:
        return None
    else:
        x_diff = h2.x - h1.x
        y_diff = h2.y - h1.y

        t1 = (h2.vx * y_diff - h2.vy * x_diff) / denom
        t2 = (h1.vx * y_diff - h1.vy * x_diff) / denom

        if t1 < 0 or t2 < 0:
            return None
        else:
            x, y = h1.x + t1 * h1.vx, h1.y + t1 * h1.vy
            return x, y


def solve_part_two(data: InputData) -> int:
    import sympy as sym

    rx, ry, rz, rvx, rvy, rvz = sym.symbols("x, y, z, vx, vy, vz")
    times = []

    eqs = []
    for idx, h in enumerate(data[:4]):
        t_i = sym.symbols(f"t_{idx}")
        times.append(t_i)
        eqs.extend([
            sym.Eq(rx + t_i * rvx, h.x + t_i * h.vx),
            sym.Eq(ry + t_i * rvy, h.y + t_i * h.vy),
            sym.Eq(rz + t_i * rvz, h.z + t_i * h.vz),
        ])

    res = sym.solve(eqs, [rx, ry, rz, rvx, rvy, rvz, *times])
    rock_x, rock_y, rock_z, *_ = res[0]

    answer = rock_x + rock_y + rock_z

    return answer


def run_tests():
    data = parse_input("data/example.txt")

    part_one = solve_part_one(data, val_min=7, val_max=27)
    print("Example - part 1:", part_one)
    assert part_one == 2

    part_two = solve_part_two(data)
    print("Example - part 2:", part_two)
    assert part_two == 47


def main():
    run_tests()

    data = parse_input("data/input.txt")

    answer_one = solve_part_one(
        data=data,
        val_min=200_000_000_000_000,
        val_max=400_000_000_000_000,
    )
    print("Part 1:", answer_one)

    answer_two = solve_part_two(data)
    print("Part 2:", answer_two)


if __name__ == "__main__":
    main()

