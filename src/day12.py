import sys
import networkx as nx

import inputfetcher
from inputparsers import parse_matrix2d
from Coordinate import Coordinate
from utils import is_on_map

EXAMPLE = """\
RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE\
"""


def parse_input(example: bool) -> list[list[str]]:
    data = EXAMPLE if example else inputfetcher.fetch_input('2024', '12')
    return parse_matrix2d(data, str)


def get_sides(p: Coordinate,
              garden: list[list[str]]) -> list[bool]:
    sides = []
    for n in p.get_neighbors():
        if is_on_map(n, garden):
            sides.append(garden[n.x][n.y] != garden[p.x][p.y])
        else:
            sides.append(True)
    return sides


def build_graph(garden: list[list[str]],
                bulk_discount: bool = False) -> nx.Graph:
    G = nx.Graph()
    x_max = len(garden) - 1
    y_max = len(garden[0]) - 1
    for i, row in enumerate(garden):
        for j, plot in enumerate(row):
            p = Coordinate(i, j)
            G.add_node(p)
            neighbors = [np for np in p.get_neighbors(x_max, y_max)]
            for n in neighbors:
                if plot == garden[n.x][n.y]:
                    d = 0
                    if bulk_discount:
                        # REVISIT: I feel like this spoils the elegance of the graph approach.
                        sides_p = get_sides(p, garden)
                        sides_n = get_sides(n, garden)
                        d = sum([a & b for (a, b) in zip(sides_p, sides_n)])
                    G.add_edge(p, n, discount=d)
    return G


def solve_1_2(garden: list[list[str]],
              bulk_discount: bool = False) -> int:
    G = build_graph(garden, bulk_discount)
    regions = list(nx.connected_components(G))
    price = 0
    for r in regions:
        area = len(r)
        sides = [4-d for _, d in G.degree(r)]
        perimeter = sum(sides)
        if bulk_discount:
            discounts = [d["discount"] for (_, _, d) in G.edges(r, data=True)]
            perimeter -= sum(discounts)
        price += area * perimeter
    return price


if __name__ == "__main__":
    use_example = "--example" in sys.argv
    garden = parse_input(use_example)
    result_1 = solve_1_2(garden, bulk_discount=False)
    if use_example:
        assert result_1 == 1930, result_1
    print(f'Result 1: {result_1}')
    result_2 = solve_1_2(garden, bulk_discount=True)
    if use_example:
        assert result_2 == 1206, result_2
    print(f'Result 2: {result_2}')
