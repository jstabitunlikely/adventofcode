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


def solve_1_cpu(numbers: list[int]) -> int:
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


def solve_1(numbers: list[int]) -> int:
    N = 2000
    MODMASK = (1 << 24) - 1  # Create a bitmask with N set bits
    secrets = [[0 for _ in range(N)] for _ in range(len(numbers))]
    for i, number in enumerate(numbers):
        secret = number
        for j in range(N):
            # 1.
            # Calculate the result of multiplying the secret number by 64.
            # Then, mix this result into the secret number.
            secret ^= (secret << 6)
            # Finally, prune the secret number.
            secret &= MODMASK
            # 2.
            # Calculate the result of dividing the secret number by 32. Round the result down to the nearest integer.
            # Then, mix this result into the secret number.
            secret ^= (secret >> 5)
            # Finally, prune the secret number.
            secret &= MODMASK
            # 3.
            # Calculate the result of multiplying the secret number by 2048.
            # Then, mix this result into the secret number.
            secret ^= (secret << 11)
            # Finally, prune the secret number.
            secret &= MODMASK
            secrets[i][j] = secret
    return sum([s[-1] for s in secrets])


if __name__ == "__main__":
    use_example = "--example" in sys.argv
    numbers = parse_input(use_example)
    result_1 = solve_1(numbers)
    if use_example:
        assert result_1 == 37327623, result_1
        result_1_cpu = solve_1_cpu(numbers)
        assert result_1_cpu == result_1, result_1_cpu
    print(f'Result 1: {result_1}')
