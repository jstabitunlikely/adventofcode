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
        junctions = self.puzzle_raw.split()
        self.puzzle = []
        for junction in junctions:
            coordinate = list(map(int, junction.split(',')))
            self.puzzle.append(Coordinate3(coordinate[0], coordinate[1], coordinate[2]))

    def solve_part_1(self) -> dict[str, int]:
        junction_pairs = list(combinations(self.puzzle, 2))
        junction_pairs_by_distance = sorted(junction_pairs, key=lambda j: j[0].get_distance_euclidean(j[1]))
        circuits = nx.Graph()
        for i, jp in enumerate(junction_pairs_by_distance):
            circuits.add_node(jp[0])
            circuits.add_node(jp[1])
            circuits.add_edge(jp[0], jp[1])
            if i == self.NOF_CONNECTIONS-1:
                circuits_size = sorted([len(cc) for cc in list(nx.connected_components(circuits))], reverse=True)
                answer_1 = reduce(lambda x, y: x * y, circuits_size[:self.NOF_CIRCUITS])
            if (len(circuits) == len(self.puzzle)) and \
                    (len(list(nx.connected_components(circuits))) == 1):
                answer_2 = jp[0].x * jp[1].x
                break
        return {
            'part_1': answer_1,
            'part_2': answer_2,
        }

    solve_part_2 = solve_part_1


def main() -> dict[str, int]:  # pragma: no cover
    today = y25d08()
    today.solve()
    return today.answer


if __name__ == "__main__":  # pragma: no cover
    answer = main()
    print(f'Part 1: {answer['part_1']}')
    print(f'Part 2: {answer['part_2']}')
