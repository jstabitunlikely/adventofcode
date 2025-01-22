from typing import Optional

from CSInstructionSet import CSInstructionSet


class CSComputer():

    def __init__(self,
                 regbank: dict[str, int],
                 instr: Optional[CSInstructionSet] = None,
                 prog: list[int] = [],
                 ) -> None:
        # Debug info
        self.stacktrace = ''

        # A register bank must be provided
        self.regbank = regbank

        # Use the default Instruction set if none provided
        if instr is None:
            self.instr = CSInstructionSet(regbank)
        else:
            self.instr = instr

        # Store the program as default if provided
        if prog is not None:
            self.prog = prog

    def run(self,
            prog: list[int] = [],
            trace: bool = False) -> list[int]:
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
                self.stacktrace += f"\t{instr_p:2d}: {instr.__name__}({operand:2d}) => A: {self.regbank['A']:10d}, B: {
                    self.regbank['B']:10d}, C: {self.regbank['C']:10d}\n"
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
