"""Day 20"""
import math
from abc import abstractmethod
from typing import NamedTuple


Pulse = bool
State = bool
HIGH = True
LOW = False


class Module:
    def __init__(self, name: str):
        self.name: str = name
        self.inputs: list[str] = []
        self.outputs: list[str] = []

    def add_input(self, input_name: str):
        self.inputs.append(input_name)

    def add_output(self, output_name: str):
        self.outputs.append(output_name)

    @abstractmethod
    def handle(self, pulse: tuple[str, Pulse]) -> list[tuple[str, Pulse]]:
        raise NotImplementedError()

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.inputs} -> {self.outputs})"


class FlipFlop(Module):
    def __init__(self, name: str):
        super().__init__(name=name)
        self.state: State = LOW

    def handle(self, pulse: tuple[str, Pulse]) -> list[tuple[str, Pulse]]:
        _, p = pulse
        if p == LOW:
            self.state = not self.state
            return [(self.name, self.state, out) for out in self.outputs]

        return []


class Conjunction(Module):
    def __init__(self, name: str):
        super().__init__(name=name)
        self.memory: dict[str, State] = {}

    def add_input(self, input_name: str):
        super().add_input(input_name)
        self.memory[input_name] = LOW

    def handle(self, pulse: tuple[str, Pulse]) -> list[tuple[str, Pulse]]:
        src, p = pulse
        self.memory[src] = p

        if all(v == HIGH for v in self.memory.values()):
            outs = [(self.name, LOW, out) for out in self.outputs]
        else:
            outs = [(self.name, HIGH, out) for out in self.outputs]

        return outs


class Broadcaster(Module):
    def __init__(self):
        super().__init__(name="broadcaster")

    def handle(self, pulse: tuple[str, Pulse]) -> list[tuple[str, Pulse]]:
        _, p = pulse
        return [(self.name, p, out) for out in self.outputs]


InputData = dict[str, FlipFlop | Conjunction | Broadcaster]


def parse_input(path: str) -> InputData:
    with open(path, "r") as fin:
        circuit = {}

        for line in fin.readlines():
            module_name, outputs = line.strip().split(" -> ")
            
            if module_name == "broadcaster":
                m = Broadcaster()
            else:
                module_type = module_name[0]
                module_name = module_name[1:]

                if module_type == "%":
                    m = FlipFlop(name=module_name)
                elif module_type == "&":
                    m = Conjunction(name=module_name)

            for out in outputs.split(", "):
                m.add_output(out)

            circuit[module_name] = m
        
        # Attach all inputs
        for input_name, module in circuit.items():
            for out in module.outputs:
                if out not in circuit:
                    continue

                circuit[out].add_input(input_name)

        return circuit


def solve_part_one(circuit: InputData) -> int:
    num_low = 0
    num_high = 0

    for _ in range(1000):
        queue = [("button", LOW, "broadcaster")]
        num_low += 1

        while queue:
            src, pulse, dst = queue.pop(0)

            if dst not in circuit:
                continue

            output_pulses = circuit[dst].handle((src, pulse))

            for s, p, d in output_pulses:
                if p == LOW:
                    num_low += 1
                else:
                    num_high += 1

            queue.extend(output_pulses)

    answer = num_low * num_high

    return answer


def solve_part_two(circuit: InputData) -> int:
    num_button_pressed = 0

    rx_input_cycle_lengths = {
        src: -1
        for name, module in circuit.items()
        for src in circuit[name].inputs
        if module.outputs[0] == "rx"
    }

    while True:
        queue = [("button", LOW, "broadcaster")]
        num_button_pressed += 1

        while queue:
            src, pulse, dst = queue.pop(0)

            if src in rx_input_cycle_lengths and pulse == HIGH:
                rx_input_cycle_lengths[src] = num_button_pressed

            if all(v != -1 for v in rx_input_cycle_lengths.values()):
                return math.lcm(*rx_input_cycle_lengths.values())

            if dst not in circuit:
                continue

            output_pulses = circuit[dst].handle((src, pulse))
            queue.extend(output_pulses)
        

def run_tests():
    data = parse_input("data/example.txt")

    part_one = solve_part_one(data)
    print("Example - part 1:", part_one)
    assert part_one == 32_000_000

    data = parse_input("data/example2.txt")

    part_one = solve_part_one(data)
    print("Example2 - part 1:", part_one)
    assert part_one == 11_687_500


def main():
    run_tests()

    data = parse_input("data/input.txt")

    answer_one = solve_part_one(data)
    print("Part 1:", answer_one)

    data = parse_input("data/input.txt")

    answer_two = solve_part_two(data)
    print("Part 2:", answer_two)


if __name__ == "__main__":
    main()

