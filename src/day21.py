import sys
import networkx as nx
from functools import cache

from Map import Map
import inputfetcher

EXAMPLE = """\
029A
980A
179A
456A
379A\
"""

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

LAYERS = ['me', 'dirpad', 'dirpad', 'numpad']


def parse_input(example: bool) -> list[str]:
    data = EXAMPLE if example else inputfetcher.fetch_input('2024', '21')
    return data.split('\n')


def parse_keypad(pad: str) -> nx.Graph:
    KEY_H = 2
    KEY_W = 4
    p = [list(p) for p in pad.split('\n')]
    K = nx.DiGraph()
    # Enumerate over all the top-left key corners
    for i, row in enumerate(p[:-1:KEY_H]):
        for j, _ in enumerate(row[:-1:KEY_W]):
            key = p[(KEY_H*i)+1][(KEY_W*j)+2]
            if key != " ":
                K.add_node(key)
    clockwise = "<^>v"
    counter_clockwise = ">v<^"
    # Enumerate over all the inner top-left key corners
    for i, row in enumerate(p[KEY_H:-1:KEY_H]):
        for j, _ in enumerate(row[KEY_W:-1:KEY_W]):
            x = KEY_H*(i+1)
            y = KEY_W*(j+1)
            keys = [
                p[x+1][y+2],  # bottom-right
                p[x+1][y-2],  # bottom-left
                p[x-1][y-2],  # top-left
                p[x-1][y+2],  # top-right
            ]
            # Add edges clockwise and counter-clockwise (diagonal edges are not possible)
            for s, (k1, k2) in enumerate(zip(keys, keys[1:] + [keys[0]])):
                if k1 == " " or k2 == " ":
                    continue
                K.add_edge(k1, k2, move=clockwise[s])
                K.add_edge(k2, k1, move=counter_clockwise[s])
    return K


def shortest_outer_sequence(sequence: str,
                            cursor: str,
                            numpad: nx.Graph,
                            dirpad: nx.Graph,
                            depth: int):
    match LAYERS[depth]:
        case 'numpad':
            pad = numpad
        case 'dirpad':
            pad = dirpad
        case 'me':
            return sequence
    edge_attributes = nx.get_edge_attributes(pad, "move")
    sequence = cursor + sequence
    outer_sequence = ''
    for key1, key2 in zip(sequence, sequence[1:]):
        paths = nx.all_shortest_paths(pad, key1, key2)
        shortseq = ''
        for path in paths:
            edges = [(k1, k2) for k1, k2 in zip(path, path[1:])]
            outseq = ''.join(edge_attributes[e] for e in edges)
            outseq += 'A'
            seq = shortest_outer_sequence(outseq, 'A', numpad, dirpad, depth-1)
            if shortseq == '' or len(seq) < len(shortseq):
                shortseq = seq
        outer_sequence += shortseq
    return outer_sequence


def solve_1(codes: list[str]) -> int:
    dirpad = parse_keypad(DIRPAD)
    numpad = parse_keypad(NUMPAD)
    complexity = 0
    for code in codes:
        sequence = shortest_outer_sequence(code, 'A', numpad, dirpad, depth=3)
        complexity += len(sequence) * int(code[:-1])
    return complexity


def solve_2(codes: list[str]) -> int:
    return 0


if __name__ == "__main__":
    use_example = "--example" in sys.argv
    codes = parse_input(use_example)
    result_1 = solve_1(codes)
    if use_example:
        assert result_1 == 126384, result_1
    print(f'Result 1: {result_1}')
    result_2 = solve_2(codes)
    if use_example:
        assert False, result_2
    print(f'Result 2: {result_2}')
