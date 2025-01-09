import re
import sys

import inputfetcher

EXAMPLE = """\
Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0\
"""


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


class Instructions():

    def __init__(self,
                 regbank) -> None:
        self.regbank = regbank

    # Combo operand

    # REVISIT: a better way without getting all register values in each call
    def combo(self, op):
        combo = [
            0, 1, 2, 3,
            self.regbank['A'],
            self.regbank['B'],
            self.regbank['C'],
            # RESERVED
        ]
        return combo[op]

    # Instructions

    def adv(self, op):
        """The adv instruction (opcode 0) performs division. The numerator is the value in the A register. The
        denominator is found by raising 2 to the power of the instruction's combo operand. (So, an operand of 2 would
        divide A by 4 (2^2); an operand of 5 would divide A by 2^B.) The result of the division operation is truncated
        to an integer and then written to the A register.
        """
        self.regbank['A'] //= 2**self.combo(op)

    def bxl(self, op):
        """The bxl instruction (opcode 1) calculates the bitwise XOR of register B and the instruction's literal
        operand, then stores the result in register B.
        """
        self.regbank['B'] ^= op

    def bst(self, op):
        """The bst instruction (opcode 2) calculates the value of its combo operand modulo 8 (thereby keeping only its
        lowest 3 bits), then writes that value to the B register.
        """
        self.regbank['B'] = self.combo(op) % 8

    def jnz(self, op):
        """The jnz instruction (opcode 3) does nothing if the A register is 0. However, if the A register is not zero,
        it jumps by setting the instruction pointer to the value of its literal operand; if this instruction jumps, the
        instruction pointer is not increased by 2 after this instruction.
        """
        if self.regbank['A']:
            return op

    def bxc(self, op):
        """The bxc instruction (opcode 4) calculates the bitwise XOR of register B and register C, then stores the
        result in register B. (For legacy reasons, this instruction reads an operand but ignores it.)
        """
        self.regbank['B'] ^= self.regbank['C']

    def out(self, op):
        """The out instruction (opcode 5) calculates the value of its combo operand modulo 8, then outputs that value.
        (If a program outputs multiple values, they are separated by commas.)
        """
        return self.combo(op) % 8

    def bdv(self, op):
        """The bdv instruction (opcode 6) works exactly like the adv instruction except that the result is stored in the
        B register. (The numerator is still read from the A register.)
        """
        self.regbank['B'] = self.regbank['A'] // 2**self.combo(op)

    def cdv(self, op):
        """The cdv instruction (opcode 7) works exactly like the adv instruction except that the result is stored in the
        C register. (The numerator is still read from the A register.)
        """
        self.regbank['C'] = self.regbank['A'] // 2**self.combo(op)


class ChronospatialComputer():

    def __init__(self,
                 regbank: dict,
                 instr: Instructions = None,
                 prog: list[int] = None,
                 ) -> None:
        self.regbank = regbank

        if instr is None:
            self.instr = Instructions(regbank)
        else:
            self.instr = instr

        if prog is not None:
            self.prog = prog

        self.decoder = [
            self.instr.adv,
            self.instr.bxl,
            self.instr.bst,
            self.instr.jnz,
            self.instr.bxc,
            self.instr.out,
            self.instr.bdv,
            self.instr.cdv,
        ]

    def run(self,
            prog: list[int] = None) -> str:
        assert prog is not None or self.prog is not None, 'Program was not provided!'
        if prog is None:
            prog = self.prog

        instr_p_max = len(prog)-1
        instr_p = 0
        out = []
        while instr_p < instr_p_max:
            opcode = prog[instr_p]
            instr = self.decoder[opcode]
            operand = prog[instr_p+1]
            result = instr(operand)
            # REVISIT: not entirely happy with this solution for jnz
            if instr == self.instr.jnz and result is not None:
                instr_p = result
            else:
                if result is not None:
                    out.append(result)
                instr_p += 2
        return ','.join([str(o) for o in out])


if __name__ == "__main__":
    use_example = "--example" in sys.argv
    prog, regbank = parse_input(use_example)
    cpu = ChronospatialComputer(regbank=regbank, prog=None)
    result_1 = cpu.run(prog)
    print(f'Result 1: {result_1}')
