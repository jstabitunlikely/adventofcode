from typing import Any
from Day import Day
import re
from itertools import combinations, combinations_with_replacement


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
                'switches_joltages': switches_joltages,
                'joltages': joltages
            })

    def solve_part_1(self) -> int:
        nof_presses_total = 0
        for machine in self.puzzle:
            found = 0
            nof_presses = 0
            # Try the shortest combinations first
            # Note: XOR is commutative, so we can go from the desired state to zero
            # Note: XOR is self-inverse and associative, so we don't actually need to press any button more than once
            while (True):
                nof_presses += 1
                # Try each combination of N presses
                for combo in list(combinations(machine['switches_lights'], nof_presses)):
                    lights = machine['lights']  # New combination of presses, reset the lights
                    # Press one by one
                    for v in combo:
                        lights ^= v
                        if not lights:
                            found = 1
                            break
                    if found:
                        break
                if found:
                    break
            if found:
                nof_presses_total += nof_presses
        return nof_presses_total

    def is_combo_valid(self, joltage: list[int], pressed: tuple[list[int]]) -> bool:
        for i, cnt in enumerate(joltage):
            i_in_pressed = [1 for sw in pressed if i in sw]
            if len(i_in_pressed) != cnt:
                return False
        return True

    def solve_part_2_example(self) -> int:
        nof_presses_total = 0
        for machine in self.puzzle:
            found = 0
            nof_presses = 0
            while (True):
                nof_presses += 1
                for combo in combinations_with_replacement(machine['switches_joltages'], nof_presses):
                    if self.is_combo_valid(machine['joltages'], combo):
                        found = 1
                        break
                if found:
                    break
            if found:
                nof_presses_total += nof_presses
        return nof_presses_total

    def solve_part_2(self) -> int:
        return self.solve_part_2_example()


def main() -> dict[str, int]:  # pragma: no cover
    today = y25d10()
    today.solve()
    return today.answer


if __name__ == "__main__":  # pragma: no cover
    answer = main()
    print(f'Part 1: {answer['part_1']}')
    print(f'Part 2: {answer['part_2']}')
