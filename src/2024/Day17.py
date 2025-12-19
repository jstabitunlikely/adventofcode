import re
from typing import Any

from Day import Day
from CSComputer import CSComputer
from CSRegbank import CSRegbank


class Day17(Day):

    def __init__(self,
                 auto_fetch: bool = True,
                 auto_parse: bool = True) -> None:
        super().__init__(year='2024', day='17', auto_fetch=auto_fetch, auto_parse=auto_parse)

    def parse_puzzle(self) -> None:
        # Get the raw strings for registers and program
        self.puzzle_raw = self.puzzle_raw.strip()
        regs, prog = self.puzzle_raw.split('\n\n')
        # Extract the program into a list
        prg_re = re.compile(r'Program: ([0-9,]+)', flags=re.DOTALL)
        prog_matches = re.findall(prg_re, prog)
        prog_split = prog_matches[0].split(',')
        prog_int = [int(p) for p in prog_split]
        # Extract the registers into a dict
        reg_re = re.compile(r'Register ([ABC]): ([0-9-]+)', flags=re.DOTALL)
        regs_matches = re.findall(reg_re, regs)
        regs_dict = dict((k, int(v)) for k, v in regs_matches)
        self.puzzle: dict[str, Any] = {
            'prog': prog_int,
            'regs': regs_dict,
        }

    def pseudocode(self,
                   A: int,
                   Amod8: int):
        # output = (((8*(A+R)) // (2**R^3)) ^ R^3 ^ 3) % 8
        regC = (8*A+Amod8) // (2**(Amod8 ^ 3))
        return ((regC ^ Amod8 ^ 3 ^ 3) % 8)

    def loop(self,
             A: int,
             expected_output: list[int],
             prog: list[int]) -> list[int]:
        # We have a possible initial value of A.
        # Run the program and see if the output matches the program code.
        if not expected_output:
            regbank = CSRegbank(regbank={'A': A, 'B': 0, 'C': 0})
            cpu = CSComputer(regbank)
            return [A] if cpu.run(prog) == prog else []

        out = expected_output.pop()

        # Using a list because multiple valid solutions are possible.
        # (Happened when working on the example, trying to get the original A back.)
        A_finals = []

        # Luckily, R can only have a handful of values, let's try them all
        for R_guess in range(8):
            if out == self.pseudocode(A, R_guess):
                A_candidate = 8*A + R_guess
                # Technically, we could test A_candidate at each step but the output
                # is short enough to check only at the end, so go for the final A.
                A_final = self.loop(A_candidate, expected_output.copy(), prog)
                A_finals.extend(A_final)
        return A_finals

    def solve_part_1(self) -> str:
        regbank = CSRegbank(self.puzzle['regs'])
        cpu = CSComputer(regbank)
        output = cpu.run(self.puzzle['prog'], trace=False)
        return ','.join([str(o) for o in output])

    def solve_part_2(self) -> int:
        regA = self.loop(0, self.puzzle['prog'].copy(), self.puzzle['prog'])
        return regA[0]


def main() -> dict[str, int]:  # pragma: no cover
    today = Day17()
    today.solve()
    return today.answer


if __name__ == "__main__":  # pragma: no cover
    answer = main()
    print(f'Part 1: {answer['part_1']}')
    print(f'Part 2: {answer['part_2']}')
