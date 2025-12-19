from Day import Day
from CSComputer import CSComputer
from CSInstructionSetExt import CSInstructionSetExt
from CSCompiler import CSCompiler
from CSRegbank import CSRegbank


class Day22(Day):

    def __init__(self,
                 auto_fetch: bool = True,
                 auto_parse: bool = True) -> None:
        super().__init__(year='2024', day='22', auto_fetch=auto_fetch, auto_parse=auto_parse)
        self.CODE = """\
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

    def parse_puzzle(self) -> None:
        self.puzzle = [int(i) for i in self.puzzle_raw.split('\n')]

    def solve_part_1_cpu(self) -> int:
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
        code = cmplr.compile_asm(asm_code=self.CODE)
        cpu = CSComputer(regbank=regbank, instr=iset)
        secret_sum = 0
        for n in self.puzzle:
            regbank.set_register('B', n)
            regbank.set_register('F', 2000)
            output = cpu.run(code, trace=False)
            secret_sum += output[0]
        return secret_sum

    def get_next_secret(self, secret: int) -> int:
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

    def solve_part_1(self) -> dict[str, int]:
        N = 2000
        # Allocate the lists beforehand for perf reasons
        secrets = [[0 for _ in range(N+1)] for _ in range(len(self.puzzle))]
        prices = [[0 for _ in range(N+1)] for _ in range(len(self.puzzle))]
        # Generate the secrets
        for i, secret in enumerate(self.puzzle):
            for j in range(N+1):
                secrets[i][j] = secret
                prices[i][j] = int(str(secret)[-1])
                secret = self.get_next_secret(secret)
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
        return {
            'part_1': secret_sum,
            'part_2': max_bananas
        }

    solve_part_2 = solve_part_1


def main() -> dict[str, int]:  # pragma: no cover
    today = Day22()
    today.solve()
    return today.answer


if __name__ == "__main__":  # pragma: no cover
    answer = main()
    print(f'Part 1: {answer['part_1']}')
    print(f'Part 2: {answer['part_2']}')
