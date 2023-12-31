"""Day 22"""
from functools import cache
from typing import NamedTuple


class Position3D(NamedTuple):
    x: int
    y: int
    z: int

    def __repr__(self) -> str:
        return f"{self.x, self.y, self.z}"


class Brick(NamedTuple):
    start: Position3D
    end: Position3D
    cubes: list[Position3D]

    @classmethod
    def from_raw(cls, raw: str) -> "Brick":
        start_raw, end_raw = raw.strip().split("~")
        start = Position3D(*[int(p) for p in start_raw.split(",")])
        end = Position3D(*[int(p) for p in end_raw.split(",")])

        return cls(start, end, [])

    def get_cubes(self) -> list[Position3D]:
        if self.cubes:
            return self.cubes

        for x in range(self.start.x, self.end.x + 1):
            for y in range(self.start.y, self.end.y + 1):
                for z in range(self.start.z, self.end.z + 1):
                    self.cubes.append(Position3D(x, y, z))
        
        return self.cubes

    def supported_by(self, occupied_positions: dict[Position3D, int]) -> list[int]:
        support_bricks = set()

        cubes = set(self.get_cubes())

        for cube in cubes:
            pos = cube.x, cube.y, cube.z - 1 
            if pos in occupied_positions and pos not in cubes:
                support_bricks.add(occupied_positions[pos])

        return list(support_bricks)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.start}-{self.end})"


InputData = list[Brick]


def parse_input(path: str) -> InputData:
    with open(path, "r") as fin:
        return [Brick.from_raw(line) for line in fin.readlines()]


def solve_part_one(data: InputData) -> int:
    fallen_bricks = simulate_falling(data)

    supported_by, supporting = get_supports(fallen_bricks)

    answer = 0

    for brick_id in supported_by.keys():
        can_be_disintegrated = all(
            len([idx for idx in supported_by[s] if idx != brick_id]) > 0
            for s in supporting[brick_id]
        )
        if can_be_disintegrated:
            answer += 1

    return answer


def solve_part_two(data: InputData) -> int:
    fallen_bricks = simulate_falling(data)

    supported_by, supporting = get_supports(fallen_bricks)

    @cache
    def _find_falling_bricks(
        idx: int,
        removed_bricks: tuple[int, ...],
    ) -> list[int]:
        would_fall = []

        for supported_brick in supporting[idx]:
            if supported_brick in removed_bricks:
                continue

            if len([
                j for j in supported_by[supported_brick] 
                if j not in removed_bricks
            ]) == 0:
                would_fall.append(supported_brick)

        for brick_id in would_fall:
            rb = tuple(set([*removed_bricks, *would_fall]))
            would_fall.extend(_find_falling_bricks(brick_id, rb))

        return would_fall

    answer = 0

    for brick_id in supporting.keys():
        answer += len(_find_falling_bricks(brick_id, (brick_id,)))

    return answer


def simulate_falling(bricks: InputData) -> InputData:
    bricks = bricks.copy()

    while True:
        changed = False

        occupied_positions = get_occupied_positions(bricks)

        # Try to move each brick downwards
        for idx, brick in enumerate(bricks):
            # Already touching the ground -> no update
            if any(z == 1 for _, _, z in brick.get_cubes()):
                continue

            # Supported by any other brick -> no update
            if any(
                (cube.x, cube.y, cube.z - 1) in occupied_positions
                and occupied_positions[(cube.x, cube.y, cube.z - 1)] != idx  # TODO
                for cube in brick.get_cubes()
            ):
                continue

            # Move downwards
            changed = True
            start_x, start_y, start_z = brick.start
            end_x, end_y, end_z = brick.end
            
            new_brick = Brick(
                start=Position3D(start_x, start_y, start_z - 1),
                end=Position3D(end_x, end_y, end_z - 1),
                cubes=[],
            )

            for cube in brick.get_cubes():
                occupied_positions.pop(cube)

            for cube in new_brick.get_cubes():
                occupied_positions[cube] = idx

            bricks[idx] = new_brick

        if not changed:
            break

    return bricks


def get_occupied_positions(bricks: InputData) -> dict[Position3D, int]:
    occupied_positions = {}

    for idx, brick in enumerate(bricks):
        for cube in brick.get_cubes():
            occupied_positions[cube] = idx

    return occupied_positions


def get_supports(
    bricks: InputData,
) -> tuple[dict[int, list[int]], dict[int, list[int]]]:
    occupied_positions = get_occupied_positions(bricks)

    supported_by = {
        idx: brick.supported_by(occupied_positions)
        for idx, brick in enumerate(bricks)
    }

    supporting = {idx: [] for idx in supported_by.keys()}
    for idx, sb in supported_by.items():
        for j in sb:
            supporting[j].append(idx)

    return supported_by, supporting


def run_tests():
    data = parse_input("data/example.txt")

    part_one = solve_part_one(data)
    print("Example - part 1:", part_one)
    assert part_one == 5

    part_two = solve_part_two(data)
    print("Example - part 2:", part_two)
    assert part_two == 7


def main():
    run_tests()

    data = parse_input("data/input.txt")

    answer_one = solve_part_one(data)
    print("Part 1:", answer_one)

    answer_two = solve_part_two(data)
    print("Part 2:", answer_two)


if __name__ == "__main__":
    main()

