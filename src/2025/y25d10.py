from typing import Any
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
        self.puzzle: list[dict[str, Any]] = []
        for match in machines:
            # Lights
            lights = int(match[0].translate(self.LIGHTS_TO_BINARY)[::-1], base=2)
            # Switches
            switch_list = match[1].split()
            switches_lights = []  # Part 1 - SUM(2^N) for a XOR operation as light toggle
            switches_joltages = []  # Part 1 - TBD for a counter increment
            for switch in switch_list:
                digit_list = switch[1:-1].split(',')
                light_toggle_positions = 0
                joltage_increments = []
                for digit in digit_list:
                    light_toggle_positions += 2**int(digit)
                    joltage_increments.append(int(digit))
                switches_lights.append(light_toggle_positions)
                switches_joltages.append(joltage_increments)
            # Joltages
            joltages = []
            for joltage in match[3].strip().split(','):
                joltages.append(int(joltage))

            self.puzzle.append({
                'lights': lights,
                'switches_lights': switches_lights,
                'switches_joltages': sorted(switches_joltages, key=lambda s: len(s)),
                'joltages': joltages
            })

    def solve_part_1(self) -> int:
        presses = 0
        for machine in self.puzzle:
            found = 0
            # Try the shortest combinations first
            # Note: XOR is self-inverse, so we don't actually need to press any button more than once
            for n in range(1, len(machine['switches_lights'])+1):
                # Try each combination of N presses
                for combo in list(combinations(machine['switches_lights'], n)):
                    lights = machine['lights']  # New combination of presses, reset the lights
                    # Press one by one
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
