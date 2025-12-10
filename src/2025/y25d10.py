from Day import Day
import re
from itertools import combinations


class y25d10(Day):

    def __init__(self,
                 auto_fetch: bool = True,
                 auto_parse: bool = True) -> None:
        self.MACHINE_RE = re.compile(r'^\[([.#]+)\](( \([0-9,]+\))+) \{([0-9,]+)\}$', re.MULTILINE)
        self.LIGHTS_TO_BINARY = str.maketrans('.#', '01')
        super().__init__(year='2025', day='10', auto_fetch=auto_fetch, auto_parse=auto_parse)

    def parse_puzzle(self) -> None:
        super().parse_puzzle()
        machines = self.MACHINE_RE.findall(self.puzzle_raw)
        self.puzzle = []
        for match in machines:
            lights = int(match[0].translate(self.LIGHTS_TO_BINARY)[::-1], base=2)
            switches = match[1].split()
            switch_values = []
            for switch in switches:
                digits = switch[1:-1].split(',')
                value = 0
                for d in digits:
                    value += 2**int(d)
                switch_values.append(value)
            self.puzzle.append({
                'lights': lights,
                'switches': switch_values,
                'joltage': match[3].strip()
            })

    def solve_part_1(self) -> int:
        presses = 0
        for machine in self.puzzle:
            found = 0
            for n in range(1, len(machine['switches'])+1):
                for combo in list(combinations(machine['switches'], n)):
                    lights = machine['lights']
                    for v in combo:
                        lights ^= v
                        if not lights:
                            found = n
                            break
                    if found:
                        break
                if found:
                    break
            if found:
                presses += found
            else:
                assert (False), ":/"
        return presses

    def solve_part_2(self) -> int:
        return 0


def main() -> dict[str, str]:  # pragma: no cover
    today = y25d10()
    today.solve()
    return today.answer


if __name__ == "__main__":  # pragma: no cover
    answer = main()
    print(f'Part 1: {answer['part_1']}')
    print(f'Part 2: {answer['part_2']}')
