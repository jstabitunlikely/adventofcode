import sys

import inputfetcher

EXAMPLE = """\
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

EXAMPLE = """\
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


def parse_input(example: bool) -> dict[str, str]:
    data = EXAMPLE if example else inputfetcher.fetch_input('2024', '24')
    inputs_str, logic_str = data.split('\n\n')
    logic: dict[str, str] = {}
    # Inputs can be used as is
    for i in inputs_str.split('\n'):
        k, v = i.split(':')
        v = v.strip()
        k = k.strip()
        logic[k] = v
    # Internal logic needs to be modified to contain proper operators
    operators = {
        'AND': '&',
        'OR': '|',
        'XOR': '^',
    }
    for l in logic_str.split('\n'):
        v, k = l.split('->')
        v = v.strip()
        k = k.strip()
        v = ' '.join(map(lambda word: operators.get(word, word), v.split()))
        logic[k] = v
    return logic


def solve_1(logic: dict[str, str]) -> int:
    local_vars: dict[str, str] = {}
    # Not bothering with sorting, just trying to evaluate whatever we can over and over
    while any(logic.values()):
        for key, value in logic.items():
            try:
                local_vars[key] = eval(str(value), local_vars)
                logic[key] = ''
            except:
                continue
    # Concatenate values of all output wires
    binary = ''
    for key, value in sorted(local_vars.items(), reverse=True):
        if key.startswith('z'):
            binary += str(value)
    number = int(binary, 2)
    return number


if __name__ == "__main__":
    use_example = "--example" in sys.argv
    input_ = parse_input(use_example)
    result_1 = solve_1(input_)
    if use_example:
        assert result_1 == 2024, result_1
    print(f'Result 1: {result_1}')
