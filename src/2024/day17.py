import re
import sys

import InputFetcher
from CSComputer import CSComputer
from CSRegbank import CSRegbank

EXAMPLE = """\
Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0\
"""

EXAMPLE_2 = """\
Register A: 2024
Register B: 0
Register C: 0

Program: 0,3,5,4,3,0\
"""


def parse_input(example: bool) -> tuple[list[int], dict[str, int]]:
    data = EXAMPLE if example else InputFetcher.fetch_input('2024', '17')
    # Get the raw strings for registers and program
    data = data.strip()
    regs, prog = data.split('\n\n')
    # Extract the program into a list
    prg_re = re.compile(r'Program: ([0-9,]+)', flags=re.DOTALL)
    prog = re.findall(prg_re, prog)
    prog = prog[0].split(',')
    prog = [int(p) for p in prog]
    # Extract the registers into a dict
    reg_re = re.compile(r'Register ([ABC]): ([0-9-]+)', flags=re.DOTALL)
    regs = re.findall(reg_re, regs)
    regs = dict((k, int(v)) for k, v in regs)
    return prog, regs


def pseudocode(A: int,
               Amod8: int):
    # output = (((8*(A+R)) // (2**R^3)) ^ R^3 ^ 3) % 8
    regC = (8*A+Amod8) // (2**(Amod8 ^ 3))
    return ((regC ^ Amod8 ^ 3 ^ 3) % 8)


def loop(A: int,
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
        if out == pseudocode(A, R_guess):
            A_candidate = 8*A + R_guess
            # Technically, we could test A_candidate at each step but the output
            # is short enough to check only at the end, so go for the final A.
            A_final = loop(A_candidate, expected_output.copy(), prog)
            A_finals.extend(A_final)
    return A_finals


def solve_1(prog: list[int],
            regs: dict[str, int]) -> str:
    regbank = CSRegbank(regs)
    cpu = CSComputer(regbank)
    output = cpu.run(prog, trace=False)
    return ','.join([str(o) for o in output])


def solve_2(prog: list[int]) -> list[int]:
    return loop(0, prog.copy(), prog)


if __name__ == "__main__":
    use_example = "--example" in sys.argv
    prog, regs = parse_input(use_example)
    result_1 = solve_1(prog, regs)
    if use_example:
        assert result_1 == '4,6,3,5,6,3,5,2,1,0', result_1
    print(f'Result 1: {result_1}')
    result_2 = solve_2(prog)
    # Don't have the solution to the second example, because it's a separate
    # problem from the actual input, so nothing to check here.
    print(f'Result 2: {result_2}')
