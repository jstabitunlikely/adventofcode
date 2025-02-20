import networkx as nx
from Day import Day


class Day23(Day):

    def __init__(self,
                 auto_fetch: bool = True,
                 auto_parse: bool = True) -> None:
        super().__init__(year='2024', day='23', auto_fetch=auto_fetch, auto_parse=auto_parse)
        self.network = None

    def parse_puzzle(self) -> None:
        pairs = []
        for pair in self.puzzle_raw.split('\n'):
            a, b = pair.split('-')
            pairs.append((a, b))
        self.puzzle = pairs

    def build_network(self) -> nx.Graph:
        N = nx.Graph()
        for n1, n2 in self.puzzle:
            if n1 in N:
                N.add_node(n1)
            if n2 in N:
                N.add_node(n2)
            N.add_edge(n1, n2)
        return N

    def solve_part_1(self) -> int:
        if self.network is None:
            self.network = self.build_network()
        three_cliques = [clq for clq in nx.enumerate_all_cliques(self.network) if len(clq) == 3]
        sizes = sum([any([node.startswith('t') for node in clq]) for clq in three_cliques])
        return sizes

    def solve_part_2(self):
        if self.network is None:
            self.build_network()
        biggest_clique = max(nx.find_cliques(self.network), key=len)  # type:ignore
        node_list = list(biggest_clique)
        node_list.sort()
        password = ','.join(node_list)
        return password


def main() -> dict[str, str]:  # pragma: no cover
    today = Day23()
    today.solve()
    return today.answer


if __name__ == "__main__":  # pragma: no cover
    answer = main()
    print(f'Part 1: {answer['part_1']}')
    print(f'Part 2: {answer['part_2']}')
