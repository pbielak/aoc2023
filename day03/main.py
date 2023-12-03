"""Day 3"""
from typing import NamedTuple


class Position(NamedTuple):
    x: int
    y: int

    def __repr__(self) -> str:
        return f"({self.x}, {self.y})"


class PartNumber(NamedTuple):
    number: int
    positions: list[Position]

    def is_adjacent_to_symbol(self, symbols: dict[Position, str]) -> bool:
        for pos in self.positions:
            for neighbor_pos in self._get_neighbor_positions(pos):
                if neighbor_pos in symbols.keys():
                    return True
        return False

    def _get_neighbor_positions(self, position: Position) -> list[Position]:
        x, y = position
        offsets = (-1, 0, 1)
        return [
            Position(x + off_x, y + off_y)
            for off_x in offsets
            for off_y in offsets
            if not (off_x == 0 and off_y == 0)
        ]


class InputData(NamedTuple):
    symbols: dict[Position, str]
    part_numbers: list[PartNumber]


def parse_input(path: str) -> InputData:
    symbols = {}
    part_numbers = []

    with open(path, "r") as fin:
        for x, line in enumerate(fin.readlines()):
            current_number = 0
            current_number_positions = []

            for y, char in enumerate(line.strip()):
                if char.isnumeric():
                    current_number = current_number * 10 + int(char)
                    current_number_positions.append(Position(x, y))
                else:
                    if current_number > 0:
                        part_numbers.append(
                            PartNumber(
                                number=current_number, 
                                positions=current_number_positions,
                            )
                        )
                        current_number = 0
                        current_number_positions = []
                    if char != ".": # is a symbol
                        symbols[Position(x, y)] = char

            if current_number > 0:
                part_numbers.append(
                    PartNumber(
                        number=current_number, 
                        positions=current_number_positions,
                    )
                )

        return InputData(
            symbols=symbols,
            part_numbers=part_numbers,
        )


def solve_part_one(data: InputData) -> int:
    answer = 0

    for part_number in data.part_numbers:
        if part_number.is_adjacent_to_symbol(data.symbols):
            answer += part_number.number

    return answer


def solve_part_two(data: InputData) -> int:
    answer = 0

    gear_positions = [k for k, v in data.symbols.items() if v == "*"]

    for gear_pos in gear_positions:
        part_numbers = [
            pn.number
            for pn in data.part_numbers
            if pn.is_adjacent_to_symbol({gear_pos: "*"})
        ]
        if len(part_numbers) == 2:
            answer += part_numbers[0] * part_numbers[1]

    return answer


def run_tests():
    data = parse_input("data/example.txt")

    part_one = solve_part_one(data)
    print("Example - part 1:", part_one)
    assert part_one == 4_361

    part_two = solve_part_two(data)
    print("Example - part 2:", part_two)
    assert part_two == 467_835


def main():
    run_tests()

    data = parse_input("data/input.txt")

    answer_one = solve_part_one(data)
    print("Part 1:", answer_one)

    answer_two = solve_part_two(data)
    print("Part 2:", answer_two)


if __name__ == "__main__":
    main()

