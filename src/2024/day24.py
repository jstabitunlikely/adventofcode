import sys

import InputFetcher
from Circuit import Circuit

EXAMPLE_1 = """\
x00: 1
x01: 1
x02: 1
y00: 0
y01: 1
y02: 0

x00 AND y00 -> z00
x01 XOR y01 -> z01
x02 OR y02 -> z02\
"""

EXAMPLE_1 = """\
x00: 1
x01: 0
x02: 1
x03: 1
x04: 0
y00: 1
y01: 1
y02: 1
y03: 1
y04: 1

ntg XOR fgs -> mjb
y02 OR x01 -> tnw
kwq OR kpj -> z05
x00 OR x03 -> fst
tgd XOR rvg -> z01
vdt OR tnw -> bfw
bfw AND frj -> z10
ffh OR nrd -> bqk
y00 AND y03 -> djm
y03 OR y00 -> psh
bqk OR frj -> z08
tnw OR fst -> frj
gnj AND tgd -> z11
bfw XOR mjb -> z00
x03 OR x00 -> vdt
gnj AND wpb -> z02
x04 AND y00 -> kjc
djm OR pbm -> qhw
nrd AND vdt -> hwm
kjc AND fst -> rvg
y04 OR y02 -> fgs
y01 AND x02 -> pbm
ntg OR kjc -> kwq
psh XOR fgs -> tgd
qhw XOR tgd -> z09
pbm OR djm -> kpj
x03 XOR y03 -> ffh
x00 XOR y04 -> ntg
bfw OR bqk -> z06
nrd XOR fgs -> wpb
frj XOR qhw -> z04
bqk OR frj -> z07
y03 OR x01 -> nrd
hwm AND bqk -> z03
tgd XOR rvg -> z12
tnw OR pbm -> gnj\
"""

EXAMPLE_2 = """\
x00: 0
x01: 1
x02: 0
x03: 1
x04: 0
x05: 1
y00: 0
y01: 0
y02: 1
y03: 1
y04: 0
y05: 1

x00 AND y00 -> z05
x01 AND y01 -> z02
x02 AND y02 -> z01
x03 AND y03 -> z03
x04 AND y04 -> z04
x05 AND y05 -> z00\
"""


def parse_input(use_example: int) -> dict[str, dict]:
    match use_example:
        case 0:
            data = InputFetcher.fetch_input('2024', '24')
        case 1:
            data = EXAMPLE_1
        case 2:
            data = EXAMPLE_2
    logic: dict[str, dict] = {
        'inputs': {},
        'gates': {},
    }
    inputs, gates = data.split('\n\n')
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
    return logic


def eval_logic(logic: dict[str, dict]) -> dict[str, str]:
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


def get_vector(local_vars: dict[str, str],
               first_char: str) -> int:
    binary = ''
    for signal, value in sorted(local_vars.items(), reverse=True):
        if signal.startswith(first_char):
            binary += str(value)
    vector = int(binary, 2)
    return vector


def solve_1_lazy(logic: dict[str, dict]) -> int:
    operators = {
        'AND': '&',
        'OR': '|',
        'XOR': '^',
    }
    for k, v in logic['gates'].items():
        v = ' '.join(map(lambda word: operators.get(word, word), v.split()))
        logic['gates'][k] = v
    local_vars = eval_logic(logic['inputs'] | logic['gates'])
    number = get_vector(local_vars, first_char='z')
    return number


def build_circuit(logic: dict[str, dict]) -> Circuit:
    circuit = Circuit()
    for o, gate in logic['gates'].items():
        a, op, b = gate.split()
        circuit.add_gate(op, [a, b], o)
    return circuit


def solve_1_2(logic: dict[str, dict]) -> tuple[int, str]:
    circuit = build_circuit(logic)
    circuit.set_input_signals(logic['inputs'])

    # Part 1
    z_value = circuit.evaluate_vector('z')

    # Part 2
    faults = []
    z_width = circuit.get_vector_width('z')
    # Circuit is a DAG representation of a Ripple-carry adder logic.
    # We can make statements about the structure of such an adder, which we can
    # use to find out-of-place gates. (Run Adders.py for visualization.)
    for gate in circuit.graph.nodes:
        # Inputs are represented as nodes as well but they're not interesting here
        if circuit.is_input(gate):
            continue
        # Some properties we'll use later
        gate_type = circuit.graph.nodes[gate]['type']
        predecessors = circuit.graph.predecessors(gate)
        successors = circuit.graph.successors(gate)
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
            if not all([circuit.is_input(p) for p in predecessors]):
                faults.append(gate)
            # Statement #3
            # Every XOR gate that is not an output (already caught be the
            # previous branch) has to have an XOR gate connected to its output,
            # except for the first bit because it's only a half adder
            elif not any([circuit.is_xor(s) for s in successors]):
                if not any([p.endswith('00') for p in predecessors]):
                    faults.append(gate)
        # Statement #4
        # Every AND gate must have an OR gate connected to its output, except
        # for the first bit because it's only a half adder
        elif gate_type == 'AND':
            if not any([p.endswith('00') for p in predecessors]):
                if not any([circuit.is_or(s) for s in successors]):
                    faults.append(gate)

    faults.sort()
    faults_str = ','.join(faults)
    return z_value, faults_str


if __name__ == "__main__":
    use_example = "--example" in sys.argv
    logic = parse_input(use_example=0)

    # Part 1
    if use_example:
        logic = parse_input(use_example=1)
    result_1, _ = solve_1_2(logic)
    if use_example:
        assert result_1 == 2024, result_1
    print(f'Result 1: {result_1}')

    # Part 2
    # Example solution has little to do with the actual problem
    if not use_example:
        __, result_2 = solve_1_2(logic)
        print(f'Result 2: {result_2}')
