import sys

import inputfetcher
from CSComputer import CSComputer
from CSInstructionSetExt import CSInstructionSetExt
from CSCompiler import CSCompiler
from CSRegbank import CSRegbank

EXAMPLE_1 = """\
1
10
100
2024\
"""

EXAMPLE_2 = """\
1
2
3
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


def parse_input(use_example: int) -> list[int]:
    match use_example:
        case 0:
            data = inputfetcher.fetch_input('2024', '22')
        case 1:
            data = EXAMPLE_1
        case 2:
            data = EXAMPLE_2
    return [int(i) for i in data.split('\n')]


def solve_1_cpu(buyers: list[int]) -> int:
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
    for n in buyers:
        regbank.set_register('B', n)
        regbank.set_register('F', 2000)
        output = cpu.run(code, trace=False)
        secret_sum += output[0]
    return secret_sum


def get_next_secret(secret: int) -> int:
    MODMASK = (1 << 24) - 1
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
    return secret


def solve_1_2(numbers: list[int]) -> tuple[int, int]:
    N = 2000
    # Allocate the lists beforehand for perf reasons
    secrets = [[0 for _ in range(N+1)] for _ in range(len(numbers))]
    prices = [[0 for _ in range(N+1)] for _ in range(len(numbers))]
    # Generate the secrets
    for i, secret in enumerate(numbers):
        for j in range(N+1):
            secrets[i][j] = secret
            prices[i][j] = int(str(secret)[-1])
            secret = get_next_secret(secret)
    # Part 1
    secret_sum = sum([s[-1] for s in secrets])
    # Part 2
    bananas_per_sequence: dict[tuple[int, int, int, int], int] = {}
    price_diffs = [[p2-p1 for p1, p2 in zip(buyer, buyer[1:])] for buyer in prices]
    for bi, d in enumerate(price_diffs):
        # Get the indicator sequences
        # REVISIT replace list comprehension with a sliding window
        sequences = [(p1, p2, p3, p4) for p1, p2, p3, p4 in zip(d, d[1:], d[2:], d[3:])]
        buys = {}
        seq_max_i = len(sequences) - 1
        # Iterate backwards, so we end up with the first price in the dictionary
        for i, seq in enumerate(sequences[::-1]):
            i_ = seq_max_i - i
            buys[seq] = prices[bi][i_+4]
        # Count the total price across the buyers
        for seq, price in buys.items():
            if seq in bananas_per_sequence.keys():
                bananas_per_sequence[seq] += price
            else:
                bananas_per_sequence[seq] = price
    max_bananas = max(bananas_per_sequence.values())
    return secret_sum, max_bananas


if __name__ == "__main__":
    use_example = "--example" in sys.argv
    numbers = parse_input(use_example=0)
    # Part 1
    if use_example:
        numbers = parse_input(use_example=1)
    result_1, _ = solve_1_2(numbers)
    if use_example:
        assert result_1 == 37327623, result_1
        result_1_cpu = solve_1_cpu(numbers)
        assert result_1_cpu == result_1, result_1_cpu
    print(f'Result 1: {result_1}')
    # Part 2
    if use_example:
        numbers = parse_input(use_example=2)
    _, result_2 = solve_1_2(numbers)
    if use_example:
        assert result_2 == 23, result_2
    print(f'Result 2: {result_2}')
