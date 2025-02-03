import sys
import networkx as nx

from Day import Day
from Map import Map
from Coordinate import Coordinate


class Day12(Day):

    def __init__(self,
                 auto_fetch: bool = True,
                 auto_parse: bool = True) -> None:
        super().__init__(year='2024', day='12', auto_fetch=auto_fetch, auto_parse=auto_parse)

    def parse_puzzle(self) -> None:
        self.puzzle = Map(self.puzzle_raw, str)

    def get_sides(self, p: Coordinate) -> list[bool]:
        plot_p = self.puzzle.get_element(p)
        sides = []
        for n, plot_n in self.puzzle.get_neighbors(p, "^>v<", check_edges=False):
            if self.puzzle.has_coordinate(n):
                sides.append(plot_n != plot_p)
            else:
                sides.append(True)
        return sides

    def build_graph(self, bulk_discount: bool = False) -> nx.Graph:
        G = nx.Graph()
        for p, plot1 in self.puzzle.enumerate_map():
            G.add_node(p)
            for n, plot2 in self.puzzle.get_neighbors(p, "^>v<"):
                if plot1 == plot2:
                    d = 0
                    if bulk_discount:
                        sides_p = self.get_sides(p)
                        sides_n = self.get_sides(n)
                        d = sum([a & b for (a, b) in zip(sides_p, sides_n)])
                    G.add_edge(p, n, discount=d)
        return G

    def solve_part_1(self, bulk_discount: bool = False) -> int:
        G = self.build_graph(bulk_discount)
        regions = list(nx.connected_components(G))
        price = 0
        for r in regions:
            area = len(r)
            sides = [4-d for _, d in list(G.degree(r))]  # type:ignore[reportCallIssue]
            perimeter = sum(sides)
            if bulk_discount:
                discounts = [d["discount"] for (_, _, d) in G.edges(r, data=True)]
                perimeter -= sum(discounts)
            price += area * perimeter
        return price

    def solve_part_2(self, bulk_discount: bool = True) -> int:
        return self.solve_part_1(bulk_discount=bulk_discount)


def main() -> dict[str, str]:  # pragma: no cover
    today = Day12()
    today.solve()
    return today.answer


if __name__ == "__main__":  # pragma: no cover
    answer = main()
    print(f'Part 1: {answer['part_1']}')
    print(f'Part 2: {answer['part_2']}')
