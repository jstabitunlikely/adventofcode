from Day import Day
import networkx as nx
from functools import cache


START_KEY = 'A'
ENTER_KEY = 'A'
assert START_KEY == ENTER_KEY, 'The solution relies on this assumption'

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


class Day21(Day):

    def __init__(self,
                 auto_fetch: bool = True,
                 auto_parse: bool = True) -> None:
        super().__init__(year='2024', day='21', auto_fetch=auto_fetch, auto_parse=auto_parse)
        self.dirpad = self.parse_keypad(DIRPAD)
        self.numpad = self.parse_keypad(NUMPAD)
        self.edge_attributes = {
            self.numpad: nx.get_edge_attributes(self.numpad, "move"),
            self.dirpad: nx.get_edge_attributes(self.dirpad, "move")
        }

    def parse_puzzle(self) -> None:
        self.puzzle = self.puzzle_raw.split('\n')

    def parse_keypad(self, pad: str) -> nx.Graph:
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

    @cache
    def shortest_outer_sequence_dfs(self,
                                    sequence: str,
                                    layers: tuple[str, ...]) -> int:
        match layers[-1]:
            case 'numpad':
                pad = self.numpad
            case 'dirpad':
                pad = self.dirpad
            case 'me':
                return len(sequence)
        sequence = START_KEY + sequence
        outer_seq_length = 0
        for key1, key2 in zip(sequence, sequence[1:]):
            paths = nx.all_shortest_paths(pad, key1, key2)
            shortest = float('inf')
            for path in paths:
                edges = [(k1, k2) for k1, k2 in zip(path, path[1:])]
                k1_k2_outseq = ''.join(self.edge_attributes[pad][e] for e in edges)
                k1_k2_outseq += ENTER_KEY
                length = self.shortest_outer_sequence_dfs(k1_k2_outseq, layers[:-1])
                if length < shortest:
                    shortest = length
            outer_seq_length += int(shortest)
        return outer_seq_length

    def solve_part_1(self, layers: list[str] = LAYERS_1) -> int:
        layers_tpl = tuple(layers)
        complexity = 0
        for code in self.puzzle:
            seq_length = self.shortest_outer_sequence_dfs(code, layers_tpl)
            complexity += seq_length * int(''.join([d for d in code if d.isdigit()]))
        return complexity

    def solve_part_2(self, layers: list[str] = LAYERS_2) -> int:
        return self.solve_part_1(layers=layers)


def main() -> dict[str, int]:  # pragma: no cover
    today = Day21()
    today.solve()
    return today.answer


if __name__ == "__main__":  # pragma: no cover
    answer = main()
    print(f'Part 1: {answer['part_1']}')
    print(f'Part 2: {answer['part_2']}')
