import re

from CSInstructionSet import CSInstructionSet


class CSCompiler():

    def __init__(self,
                 instruction_et: CSInstructionSet) -> None:
        self.instruction_re = re.compile(r'([a-z]{3})\(([0-9]+)\)')
        self.iset = instruction_et
        self.opcodes = {}
        for icode, iname in enumerate(self.iset.decoder):
            self.opcodes[iname.__name__] = icode

    def compile_asm(self, asm_code: str) -> list[int]:
        machine_code: list[int] = []
        asm = asm_code.split('\n')
        for line in asm:
            if m := re.match(self.instruction_re, line):
                opcode = self.opcodes[m.group(1)]
                operand = int(m.group(2))
                machine_code.extend([opcode, operand])
        return machine_code
