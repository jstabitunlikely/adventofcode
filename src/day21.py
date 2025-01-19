import sys
import networkx as nx

import inputfetcher

EXAMPLE = """\
029A
980A
179A
456A
379A\
"""

START_KEY = 'A'

NUMPAD = """\
+---+---+---+
| 7 | 8 | 9 |
+---+---+---+
| 4 | 5 | 6 |
+---+---+---+
| 1 | 2 | 3 |
+---+---+---+
    | 0 | A |
    +---+---+\
"""

DIRPAD = """\
    +---+---+
    | ^ | A |
+---+---+---+
| < | v | > |
+---+---+---+\
"""

LAYERS_1 = ['me'] + ['dirpad'] * 2 + ['numpad']
LAYERS_2 = ['me'] + ['dirpad'] * 25 + ['numpad']


def parse_input(example: bool) -> list[str]:
    data = EXAMPLE if example else inputfetcher.fetch_input('2024', '21')
    return data.split('\n')


def parse_keypad(pad: str) -> nx.Graph:
    # Key height and width on the keypad
    # Assuming key labels are in the middle of the key
    KH = 2
    KW = 4
    p = [list(p) for p in pad.split('\n')]
    K = nx.DiGraph()
    # Enumerate over all the top-left key corners
    for i, row in enumerate(p[:-KH:KH]):
        for j, _ in enumerate(row[:-KW:KW]):
            key = p[(KH*i)+KH//2][(KW*j)+KW//2]
            if key != " ":
                K.add_node(key)
    moves = "<^>v"
    # Enumerate over all the inner top-left key corners
    for i, row in enumerate(p[KH:-KH:KH]):
        for j, _ in enumerate(row[KW:-KW:KW]):
            x = KH*(i+1)
            y = KW*(j+1)
            keys = [
                # In the order of moves above
                p[x+KH//2][y+KW//2],  # bottom-right
                p[x+KH//2][y-KW//2],  # bottom-left
                p[x-KH//2][y-KW//2],  # top-left
                p[x-KH//2][y+KW//2],  # top-right
            ]
            # Add edges clockwise and counter-clockwise (diagonal edges are not possible)
            # Wrap around, so the circle is complete
            for s, (k1, k2) in enumerate(zip(keys, keys[1:] + [keys[0]])):
                if k1 == " " or k2 == " ":
                    continue
                K.add_edge(k1, k2, move=moves[s])
                K.add_edge(k2, k1, move=moves[(s+2) % len(moves)])
    return K


def shortest_outer_sequence(sequence: str,
                            depth: int):
    match layers[depth]:
        case 'numpad':
            pad = numpad
        case 'dirpad':
            pad = dirpad
        case 'me':
            return sequence
    edge_attributes = nx.get_edge_attributes(pad, "move")
    sequence = START_KEY + sequence
    outer_sequence = ''
    for key1, key2 in zip(sequence, sequence[1:]):
        paths = nx.all_shortest_paths(pad, key1, key2)
        k1_k2_seq = ''
        for path in paths:
            edges = [(k1, k2) for k1, k2 in zip(path, path[1:])]
            outseq = ''.join(edge_attributes[e] for e in edges)
            outseq += START_KEY
            seq = shortest_outer_sequence(outseq, depth-1)
            if k1_k2_seq == '' or len(seq) < len(k1_k2_seq):
                k1_k2_seq = seq
        outer_sequence += k1_k2_seq
    return outer_sequence


def solve_1_2(codes: list[str]) -> int:
    complexity = 0
    depth = len(layers)-1
    for code in codes:
        sequence = shortest_outer_sequence(code, depth)
        complexity += len(sequence) * int(''.join([d for d in code if d.isdigit()]))
    return complexity


if __name__ == "__main__":
    use_example = "--example" in sys.argv
    codes = parse_input(use_example)
    global dirpad
    dirpad = parse_keypad(DIRPAD)
    global numpad
    numpad = parse_keypad(NUMPAD)
    global layers
    layers = LAYERS_1
    result_1 = solve_1_2(codes)
    if use_example:
        assert result_1 == 126384, result_1
    print(f'Result 1: {result_1}')
    layers = LAYERS_2
    result_2 = solve_1_2(codes)
    print(f'Result 2: {result_2}')
