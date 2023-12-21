"""Day 19"""
from typing import Literal, NamedTuple


class ComparisonRule(NamedTuple):
    param_name: str
    operator: Literal["<", ">"]
    threshold: int
    destination: str

    @classmethod
    def from_raw(cls, raw: str) -> "ComparisonRule":
        cond, destination = raw.split(":")
        param_name = cond[0]
        operator = cond[1]
        threshold = int(cond[2:])

        return cls(param_name, operator, threshold, destination)

    def matches(self, part: "Part") -> bool:
        part_value = getattr(part, self.param_name)

        if self.operator == "<":
            return part_value < self.threshold
        else:
            return part_value > self.threshold


class JumpRule(NamedTuple):
    destination: str

    def matches(self, part: "Part") -> bool:
        return True


class Part(NamedTuple):
    x: int
    m: int
    a: int
    s: int

    @classmethod
    def from_raw(cls, raw: str) -> "Part":
        kwargs = {}

        for param in raw[1:-1].split(","):
            k, v = param.split("=")
            kwargs[k] = int(v)

        return cls(**kwargs)


Rules = list[ComparisonRule | JumpRule]
Workflows = dict[str, Rules]


class InputData(NamedTuple):
    workflows: Workflows 
    parts: list[Part]



def parse_input(path: str) -> InputData:
    with open(path, "r") as fin:
        workflows_raw, parts_raw = fin.read().strip().split("\n\n")

        workflows = {}
        for line in workflows_raw.split("\n"):
            idx = line.index("{")
            name = line[:idx]
            rules = [
                ComparisonRule.from_raw(raw)
                if any(op in raw for op in (">", "<"))
                else JumpRule(raw)
                for raw in line[idx + 1:-1].split(",")
            ]

            workflows[name] = rules

        parts = [Part.from_raw(raw) for raw in parts_raw.split("\n")]

        return InputData(workflows=workflows, parts=parts)


def solve_part_one(data: InputData) -> int:
    answer = 0

    for part in data.parts:
        res = apply_workflows(part, workflows=data.workflows)
        if res == "A":
            answer += part.x + part.m + part.a + part.s

    return answer


def apply_workflows(part: Part, workflows: Workflows) -> str:
    def _apply_rules(rules: Rules) -> str:
        for rule in rules:
            if rule.matches(part):
                return rule.destination

        raise RuntimeError("Should be unreachable")

    key = "in"

    while True:
        if key in ("A", "R"):
            return key

        key = _apply_rules(workflows[key])

    raise RuntimeError("Should be unreachable")


def solve_part_two(data: InputData) -> int:
    return count_accepted_combinations(
        key="in",
        workflows=data.workflows,
        param_ranges={
            "x": (1, 4000),
            "m": (1, 4000),
            "a": (1, 4000),
            "s": (1, 4000),
        },
    )


def count_accepted_combinations(
    key: str,
    workflows: Workflows,
    param_ranges: dict[str, int],
) -> int:
    def _prod(c: dict[str, int]) -> int:
        out = 1

        for k, (v_min, v_max) in c.items():
            out *= max(0, v_max - v_min + 1)

        return out

    updates = 0

    num_rules = len(workflows[key])
    rule_param_ranges = [param_ranges.copy() for _ in range(num_rules)]

    for idx, rule in enumerate(workflows[key]):
        if isinstance(rule, ComparisonRule):
            p = rule.param_name

            v_min, v_max = rule_param_ranges[idx][p]

            if rule.operator == "<":
                rule_param_ranges[idx][p] = (v_min, rule.threshold - 1)

                for i in range(idx + 1, num_rules):
                    rule_param_ranges[i][p] = (rule.threshold, v_max)

            else:  # operator: >
                rule_param_ranges[idx][p] = (rule.threshold + 1, v_max)

                for i in range(idx + 1, num_rules):
                    rule_param_ranges[i][p] = (v_min, rule.threshold)

        if rule.destination == "A":
            updates += _prod(rule_param_ranges[idx])
        elif rule.destination != "R":
            updates += count_accepted_combinations(
                key=rule.destination,
                workflows=workflows,
                param_ranges=rule_param_ranges[idx],
            )

    return updates


def run_tests():
    data = parse_input("data/example.txt")

    part_one = solve_part_one(data)
    print("Example - part 1:", part_one)
    assert part_one == 19_114

    part_two = solve_part_two(data)
    print("Example - part 2:", part_two)
    assert part_two == 167_409_079_868_000


def main():
    run_tests()

    data = parse_input("data/input.txt")

    answer_one = solve_part_one(data)
    print("Part 1:", answer_one)

    answer_two = solve_part_two(data)
    print("Part 2:", answer_two)


if __name__ == "__main__":
    main()

