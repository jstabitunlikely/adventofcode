import sys

import inputfetcher
from CSComputer import CSComputer
from CSInstructionSetExt import CSInstructionSetExt
from CSCompiler import CSCompiler
from CSRegbank import CSRegbank

EXAMPLE = """\
1
10
100
2024\
"""

CODE = """\
bsl(4) // multiply regB by 2**regA, store in regC
bxc(0) // regB xor regC, store in regB
bst(5) // regB[0:24], sore in regB
\
bdv(7) // regB//2**regD, sore in regB
bxc(0) // regB xor regC, store in regB
bst(5) // regB[0:24], sore in regB
\
bsl(8) // multiply regB by 2**regE, store in regC
bxc(0) // regB xor regC, store in regB
bst(5) // regB[0:24], sore in regB
\
fdc(9) // decrement regF, store in regF
jnz(0) // jump to 0 if regF true
out(5) // output regB\
"""


def parse_input(example: bool) -> list[int]:
    data = EXAMPLE if example else inputfetcher.fetch_input('2024', '22')
    return [int(i) for i in data.split('\n')]


def solve_1(numbers: list[int]) -> int:
    regbank = CSRegbank({
        'A': 6,
        'B': 0,     # input number
        'C': 0,
        'D': 5,
        'E': 11,
        'F': 0      # input repeats
    })
    iset = CSInstructionSetExt(regbank=regbank, modulo=24)
    cmplr = CSCompiler(instruction_et=iset)
    code = cmplr.compile_asm(asm_code=CODE)
    cpu = CSComputer(regbank=regbank, instr=iset)
    secret_sum = 0
    for n in numbers:
        regbank.set_register('B', n)
        regbank.set_register('F', 2000)
        output = cpu.run(code, trace=False)
        secret_sum += output[0]
    return secret_sum


if __name__ == "__main__":
    use_example = "--example" in sys.argv
    numbers = parse_input(use_example)
    result_1 = solve_1(numbers)
    if use_example:
        assert result_1 == 37327623, result_1
    print(f'Result 1: {result_1}')
