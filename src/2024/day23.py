import sys
import networkx as nx

import inputfetcher

EXAMPLE = """\
kh-tc
qp-kh
de-cg
ka-co
yn-aq
qp-ub
cg-tb
vc-aq
tb-ka
wh-tc
yn-cg
kh-ub
ta-co
de-co
tc-td
tb-wq
wh-td
ta-ka
td-qp
aq-cg
wq-ub
ub-vc
de-ta
wq-aq
wq-vc
wh-yn
ka-de
kh-ta
co-tc
wh-qp
tb-vc
td-yn\
"""


def parse_input(example: bool) -> list[tuple[str, str]]:
    data = EXAMPLE if example else inputfetcher.fetch_input('2024', '23')
    pairs = []
    for pair in data.split('\n'):
        a, b = pair.split('-')
        pairs.append((a, b))
    return pairs


def build_network(pairs: list[tuple[str, str]]) -> nx.Graph:
    N = nx.Graph()
    for n1, n2 in pairs:
        if n1 in N:
            N.add_node(n1)
        if n2 in N:
            N.add_node(n2)
        N.add_edge(n1, n2)
    return N


def solve_1_2(pairs: list[tuple[str, str]]) -> tuple[int, str]:
    network = build_network(pairs)
    # Part 1
    three_cliques = [clq for clq in nx.enumerate_all_cliques(network) if len(clq) == 3]
    sizes = sum([any([node.startswith('t') for node in clq]) for clq in three_cliques])
    # Part 2
    biggest_clique = max(nx.find_cliques(network), key=len)
    node_list = list(biggest_clique)
    node_list.sort()
    password = ','.join(node_list)
    return sizes, password


if __name__ == "__main__":
    use_example = "--example" in sys.argv
    pairs = parse_input(use_example)
    result_1, result_2 = solve_1_2(pairs)
    if use_example:
        assert result_1 == 7, result_1
        assert result_2 == 'co,de,ka,ta', result_2
    print(f'Result 1: {result_1}')
    print(f'Result 2: {result_2}')
