from Day import Day
from Coordinate3 import Coordinate3
from itertools import combinations
from functools import reduce
import networkx as nx


class y25d08(Day):

    def __init__(self,
                 auto_fetch: bool = True,
                 auto_parse: bool = True,
                 nof_connections: int = 1000) -> None:
        super().__init__(year='2025', day='08', auto_fetch=auto_fetch, auto_parse=auto_parse)
        self.NOF_CONNECTIONS = nof_connections
        self.NOF_CIRCUITS = 3

    def parse_puzzle(self) -> None:
        super().parse_puzzle()
        lines = self.puzzle_raw.split()
        self.puzzle = []
        for line in lines:
            coordinates = list(map(int, line.split(',')))
            self.puzzle.append(Coordinate3(coordinates[0], coordinates[1], coordinates[2]))

    def solve_part_1(self) -> int:
        junction_pairs = list(combinations(self.puzzle, 2))
        junction_pairs_by_distance = sorted(junction_pairs, key=lambda j: j[0].get_distance_euclidean(j[1]))
        junktion_pairs_top = junction_pairs_by_distance[:self.NOF_CONNECTIONS]
        circuits = nx.Graph()
        for jp in junktion_pairs_top:
            circuits.add_node(jp[0])
            circuits.add_node(jp[1])
            circuits.add_edge(jp[0], jp[1])
        circuits_size = sorted([len(cc) for cc in list(nx.connected_components(circuits))], reverse=True)
        return reduce(lambda x, y: x * y, circuits_size[:self.NOF_CIRCUITS])

    def solve_part_2(self) -> int:
        return 0


def main() -> dict[str, str]:  # pragma: no cover
    today = y25d08()
    today.solve()
    return today.answer


if __name__ == "__main__":  # pragma: no cover
    answer = main()
    print(f'Part 1: {answer['part_1']}')
    print(f'Part 2: {answer['part_2']}')
