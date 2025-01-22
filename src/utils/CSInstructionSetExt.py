from CSInstructionSet import CSInstructionSet
from CSRegbank import CSRegbank


class CSInstructionSetExt(CSInstructionSet):

    def __init__(self,
                 regbank: CSRegbank,
                 modulo: int = 8) -> None:
        super().__init__(regbank, modulo)
        self.decoder += [
            self.bsl,   # OPCODE 8
            self.fdc,   # OPCODE 9
        ]

    # New instructions

    def bsl(self, op: int) -> list:
        """The bsl instruction (opcode 8) shifts the value of B register by its combo operand, then writes
        that value to the C register."""
        self.regbank.regbank['C'] = self.regbank.regbank['B'] << self.combo(op)
        return []

    # Overloaded instructions

    def bdv(self, op: int) -> list:
        """The bdv instruction (opcode 6) works exactly like the adv instruction except that the result is stored in the
        B register and the numerator is read from the A register.
        """
        self.regbank.regbank['C'] = self.regbank.regbank['B'] >> self.combo(op)
        return []

    def out(self, op: int) -> list:
        """The out instruction (opcode 5) outputs the value of its combo operand."""
        return [self.combo(op)]

    def jnz(self, op: int) -> list:
        """The jnz instruction (opcode 3) does nothing if the F register is 0. However, if the F register is not zero,
        it jumps by setting the instruction pointer to the value of its literal operand; if this instruction jumps, the
        instruction pointer is not increased by 2 after this instruction.
        """
        if self.regbank.regbank['F']:
            return [0, op]
        return []

    def fdc(self, op: int) -> list:
        """The fdc instruction (opcode 9) decrements the value of its combo operand by 1 and stores it in F register.
        Underflow is not allowed.
        """
        self.regbank.regbank['F'] = max(0, self.combo(op) - 1)
        return []
