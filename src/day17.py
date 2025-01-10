import inputfetcher
import re
import sys


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


class Instructions():

    def __init__(self, regbank: dict[str:int]) -> None:
        self.regbank = regbank

        self.decoder = [
            self.adv,
            self.bxl,
            self.bst,
            self.jnz,
            self.bxc,
            self.out,
            self.bdv,
            self.cdv,
        ]

    # Combo operand

    # REVISIT: a better way without getting all register values in each call
    def combo(self, op: int) -> int:
        combo = [
            0, 1, 2, 3,
            self.regbank['A'],
            self.regbank['B'],
            self.regbank['C'],
            # RESERVED
        ]
        try:
            return combo[op]
        except IndexError:
            return -1

    # Instructions

    def adv(self, op: int) -> list:
        """The adv instruction (opcode 0) performs division. The numerator is the value in the A register. The
        denominator is found by raising 2 to the power of the instruction's combo operand. (So, an operand of 2 would
        divide A by 4 (2^2); an operand of 5 would divide A by 2^B.) The result of the division operation is truncated
        to an integer and then written to the A register.
        """
        self.regbank['A'] //= 2**self.combo(op)
        return []

    def bxl(self, op: int) -> list:
        """The bxl instruction (opcode 1) calculates the bitwise XOR of register B and the instruction's literal
        operand, then stores the result in register B.
        """
        self.regbank['B'] ^= op
        return []

    def bst(self, op: int) -> list:
        """The bst instruction (opcode 2) calculates the value of its combo operand modulo 8 (thereby keeping only its
        lowest 3 bits), then writes that value to the B register.
        """
        self.regbank['B'] = self.combo(op) % 8
        return []

    def jnz(self, op: int) -> list:
        """The jnz instruction (opcode 3) does nothing if the A register is 0. However, if the A register is not zero,
        it jumps by setting the instruction pointer to the value of its literal operand; if this instruction jumps, the
        instruction pointer is not increased by 2 after this instruction.
        """
        if self.regbank['A']:
            return [0, op]
        return []

    def bxc(self, op: int) -> list:
        """The bxc instruction (opcode 4) calculates the bitwise XOR of register B and register C, then stores the
        result in register B. (For legacy reasons, this instruction reads an operand but ignores it.)
        """
        self.regbank['B'] ^= self.regbank['C']
        return []

    def out(self, op: int) -> list:
        """The out instruction (opcode 5) calculates the value of its combo operand modulo 8, then outputs that value.
        (If a program outputs multiple values, they are separated by commas.)
        """
        return [self.combo(op) % 8]

    def bdv(self, op: int) -> list:
        """The bdv instruction (opcode 6) works exactly like the adv instruction except that the result is stored in the
        B register. (The numerator is still read from the A register.)
        """
        self.regbank['B'] = self.regbank['A'] // 2**self.combo(op)
        return []

    def cdv(self, op: int) -> list:
        """The cdv instruction (opcode 7) works exactly like the adv instruction except that the result is stored in the
        C register. (The numerator is still read from the A register.)
        """
        self.regbank['C'] = self.regbank['A'] // 2**self.combo(op)
        return []


class ChronospatialComputer():

    def __init__(self,
                 regbank: dict[str:int],
                 instr: Instructions = None,
                 prog: list[int] = None,
                 ) -> None:
        # Debug info
        self.stacktrace = ''

        # A register bank must be provided
        self.regbank = regbank

        # Use the default Instruction set if none provided
        if instr is None:
            self.instr = Instructions(regbank)
        else:
            self.instr = instr

        # Store the program as default if provided
        if prog is not None:
            self.prog = prog

    def run(self,
            prog: list[int] = None,
            trace: bool = False) -> str:
        assert prog is not None or self.prog is not None, 'Program was not provided!'
        # Run the default program if none is provided
        if prog is None:
            prog = self.prog

        # Debug info
        if trace:
            self.stacktrace += f'Program: {prog}\n'
            for instr_p, (opcode, operand) in enumerate(zip(prog[::2], prog[1::2])):
                instr = self.instr.decoder[opcode]
                self.stacktrace += f'\t{instr_p:2d}: {instr.__name__} {operand:2d}\n'

        instr_p_max = len(prog)-1
        instr_p = 0
        out = []
        if trace:
            self.stacktrace += 'Stack:\n'
        while instr_p < instr_p_max:
            # Fetch the opcode
            opcode = prog[instr_p]
            # Decode the opcode
            instr = self.instr.decoder[opcode]
            # Get the operand
            operand = prog[instr_p+1]
            # Execute the instruction
            result = instr(operand)
            if trace:
                self.stacktrace += f"\t{instr_p:2d}: {instr.__name__}({operand:2d}) => A: {self.regbank['A']:10d}, B: {self.regbank['B']:10d}, C: {self.regbank['C']:10d}\n"
            # Use the results
            result_len = len(result)
            # Flow control instructions have longer results
            if result_len > 1:
                instr_p = result[1]
            # Arithmetic instructions have shorter results
            else:
                instr_p += 2
                out.extend(result)
        if trace:
            print(self.stacktrace)
        return out


def parse_input(example: bool) -> tuple[list[int], dict[str:int]]:
    data = EXAMPLE if example else inputfetcher.fetch_input('2024', '17')
    # Get the raw strings for registers and program
    data = data.strip()
    regbank, prog = data.split('\n\n')
    # Extract the program into a list
    prg_re = re.compile(r'Program: ([0-9,]+)', flags=re.DOTALL)
    prog = re.findall(prg_re, prog)
    prog = prog[0].split(',')
    prog = [int(p) for p in prog]
    # Extract the registers into a dict
    reg_re = re.compile(r'Register ([ABC]): ([0-9-]+)', flags=re.DOTALL)
    regbank = re.findall(reg_re, regbank)
    regbank = dict((k, int(v)) for k, v in regbank)
    return prog, regbank


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
        cpu = ChronospatialComputer(regbank={'A': A, 'B': 0, 'C': 0})
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
            regbank: dict[str:int]) -> str:
    cpu = ChronospatialComputer(regbank)
    output = cpu.run(prog, trace=True)
    return ','.join([str(o) for o in output])


def solve_2(prog: list[int]) -> list[int]:
    return loop(0, prog.copy(), prog)


if __name__ == "__main__":
    use_example = "--example" in sys.argv
    prog, regbank = parse_input(use_example)
    result_1 = solve_1(prog, regbank)
    print(f'Result 1: {result_1}')
    result_2 = solve_2(prog)
    print(f'Result 2: {result_2}')
