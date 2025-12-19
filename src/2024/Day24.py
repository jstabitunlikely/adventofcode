from typing import Optional
from Day import Day
from Circuit import Circuit


class Day24(Day):

    def __init__(self,
                 auto_fetch: bool = True,
                 auto_parse: bool = True) -> None:
        super().__init__(year='2024', day='24', auto_fetch=auto_fetch, auto_parse=auto_parse)
        self.circuit: Optional[Circuit] = None

    def parse_puzzle(self) -> None:
        logic: dict[str, dict] = {
            'inputs': {},
            'gates': {},
        }
        inputs, gates = self.puzzle_raw.split('\n\n')
        inputs = inputs.strip()
        for i in inputs.split('\n'):
            k, v = i.split(':')
            v = v.strip()
            k = k.strip()
            logic['inputs'][k] = v
        gates = gates.strip()
        for line in gates.split('\n'):
            v, k = line.split('->')
            v = v.strip()
            k = k.strip()
            logic['gates'][k] = v
        self.puzzle = logic

    def eval_logic(self, logic: dict[str, dict]) -> dict[str, str]:
        local_vars: dict[str, str] = {}
        # Not bothering with sorting, just trying to evaluate whatever we can over and over
        # Note: local_vars has an extra key
        while len(local_vars) != len(logic) + 1:
            for key, value in logic.items():
                try:
                    local_vars[key] = eval(str(value), globals=local_vars)
                except NameError:
                    continue
        return local_vars

    def get_vector(self, local_vars: dict[str, str],
                   first_char: str) -> int:
        binary = ''
        for signal, value in sorted(local_vars.items(), reverse=True):
            if signal.startswith(first_char):
                binary += str(value)
        vector = int(binary, 2)
        return vector

    def solve_1_lazy(self, logic: dict[str, dict]) -> int:
        operators = {
            'AND': '&',
            'OR': '|',
            'XOR': '^',
        }
        for k, v in logic['gates'].items():
            v = ' '.join(map(lambda word: operators.get(word, word), v.split()))
            logic['gates'][k] = v
        local_vars = self.eval_logic(logic['inputs'] | logic['gates'])
        number = self.get_vector(local_vars, first_char='z')
        return number

    def build_circuit(self) -> None:
        self.circuit = Circuit()
        for o, gate in self.puzzle['gates'].items():
            a, op, b = gate.split()
            self.circuit.add_gate(op, [a, b], o)

    def solve_part_1(self) -> int:
        if self.circuit is None:
            self.build_circuit()
        assert self.circuit is not None
        self.circuit.set_input_signals(self.puzzle['inputs'])
        z_value = self.circuit.evaluate_vector('z')
        return z_value

    def solve_part_2(self) -> str:
        if self.circuit is None:
            self.build_circuit()
        assert self.circuit is not None
        faults = []
        z_width = self.circuit.get_vector_width('z')
        # Circuit is a DAG representation of a Ripple-carry adder logic.
        # We can make statements about the structure of such an adder, which we can
        # use to find out-of-place gates. (Run Adders.py for visualization.)
        for gate in self.circuit.graph.nodes:
            # Inputs are represented as nodes as well but they're not interesting here
            if self.circuit.is_input(gate):
                continue
            # Some properties we'll use later
            gate_type = self.circuit.graph.nodes[gate]['type']
            predecessors = self.circuit.graph.predecessors(gate)
            successors = self.circuit.graph.successors(gate)
            # Statement 1
            # Every output gate  must be an XOR gate (S), except for the last one.
            # Because it's a Cout, it must be an AND gate.
            if gate.startswith('z'):
                if gate == f'z{z_width:02d}':
                    if gate_type != 'OR':
                        faults.append(gate)
                elif gate_type != 'XOR':
                    faults.append(gate)
            # Statement 2-3
            elif gate_type == 'XOR':
                # Statement 2
                # Every XOR gate that is not an output (already caught be the
                # previous branch) has to have inputs signals connected to it
                if not all([self.circuit.is_input(p) for p in predecessors]):
                    faults.append(gate)
                # Statement #3
                # Every XOR gate that is not an output (already caught be the
                # previous branch) has to have an XOR gate connected to its output,
                # except for the first bit because it's only a half adder
                elif not any([self.circuit.is_xor(s) for s in successors]):
                    if not any([p.endswith('00') for p in predecessors]):
                        faults.append(gate)
            # Statement #4
            # Every AND gate must have an OR gate connected to its output, except
            # for the first bit because it's only a half adder
            elif gate_type == 'AND':
                if not any([p.endswith('00') for p in predecessors]):
                    if not any([self.circuit.is_or(s) for s in successors]):
                        faults.append(gate)

        faults.sort()
        faults_str = ','.join(faults)
        return faults_str


def main() -> dict[str, int]:  # pragma: no cover
    today = Day24()
    today.solve()
    return today.answer


if __name__ == "__main__":  # pragma: no cover
    answer = main()
    print(f'Part 1: {answer['part_1']}')
    print(f'Part 2: {answer['part_2']}')
