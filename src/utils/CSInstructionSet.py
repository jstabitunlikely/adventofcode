from CSRegbank import CSRegbank


class CSInstructionSet():

    def __init__(self,
                 regbank: CSRegbank,
                 modulo: int = 3) -> None:
        self.MODMASK = (1 << modulo) - 1  # Create a bitmask with N set bits
        self.regbank = regbank

        self.decoder = [
            self.adv,   # OPCODE 0
            self.bxl,   # OPCODE 1
            self.bst,   # OPCODE 2
            self.jnz,   # OPCODE 3
            self.bxc,   # OPCODE 4
            self.out,   # OPCODE 5
            self.bdv,   # OPCODE 6
            self.cdv,   # OPCODE 7
        ]

    # Combo operand

    # REVISIT: a better way without getting all register values in each call
    def combo(self, op: int) -> int:
        combo = [0, 1, 2, 3]
        combo.extend([reg for _, reg in sorted(self.regbank.regbank.items())])
        return combo[op]

    # Instructions

    def adv(self, op: int) -> list:
        """The adv instruction (opcode 0) performs division. The numerator is the value in the A register. The
        denominator is found by raising 2 to the power of the instruction's combo operand. (So, an operand of 2 would
        divide A by 4 (2^2); an operand of 5 would divide A by 2^B.) The result of the division operation is truncated
        to an integer and then written to the A register.
        """
        self.regbank.regbank['A'] >>= self.combo(op)
        return []

    def bxl(self, op: int) -> list:
        """The bxl instruction (opcode 1) calculates the bitwise XOR of register B and the instruction's literal
        operand, then stores the result in register B.
        """
        self.regbank.regbank['B'] ^= op
        return []

    def bst(self, op: int) -> list:
        """The bst instruction (opcode 2) calculates the value of its combo operand modulo 8 (thereby keeping only its
        lowest 3 bits), then writes that value to the B register.
        """
        self.regbank.regbank['B'] = self.combo(op) & self.MODMASK
        return []

    def jnz(self, op: int) -> list:
        """The jnz instruction (opcode 3) does nothing if the A register is 0. However, if the A register is not zero,
        it jumps by setting the instruction pointer to the value of its literal operand; if this instruction jumps, the
        instruction pointer is not increased by 2 after this instruction.
        """
        if self.regbank.regbank['A']:
            return [0, op]
        return []

    def bxc(self, op: int) -> list:
        """The bxc instruction (opcode 4) calculates the bitwise XOR of register B and register C, then stores the
        result in register B. (For legacy reasons, this instruction reads an operand but ignores it.)
        """
        self.regbank.regbank['B'] ^= self.regbank.regbank['C']
        return []

    def out(self, op: int) -> list:
        """The out instruction (opcode 5) calculates the value of its combo operand modulo 8, then outputs that value.
        (If a program outputs multiple values, they are separated by commas.)
        """
        return [self.combo(op) & self.MODMASK]

    def bdv(self, op: int) -> list:
        """The bdv instruction (opcode 6) works exactly like the adv instruction except that the result is stored in the
        B register. (The numerator is still read from the A register.)
        """
        self.regbank.regbank['B'] = self.regbank.regbank['A'] >> self.combo(op)
        return []

    def cdv(self, op: int) -> list:
        """The cdv instruction (opcode 7) works exactly like the adv instruction except that the result is stored in the
        C register. (The numerator is still read from the A register.)
        """
        self.regbank.regbank['C'] = self.regbank.regbank['A'] >> self.combo(op)
        return []
