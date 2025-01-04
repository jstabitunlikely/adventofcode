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

EXAMPLE = """\
AAAA
BBCD
BBCC
EEEC\
"""


def parse_input(example: bool) -> list[list[str]]:
    data = EXAMPLE if example else inputfetcher.fetch_input('2024', '12')
    return parse_matrix2d(data, str)


def solve_1_2(garden: list[list[str]],
              bulk_discount: bool = False) -> int:
    G = nx.Graph()
    for i, row in enumerate(garden):
        for j, plot in enumerate(row):
            p = Coordinate(i, j)
            G.add_node(p)
            neighbors = [np for np in p.get_neighbor_coordinates() if is_on_map(np, garden)]
            G.add_edges_from([(p, n) for n in neighbors if plot == garden[n.x][n.y]])
    regions = list(nx.connected_components(G))
    price = 0
    for r in regions:
        area = len(r)
        if bulk_discount:
            # TODO: handle bulk discount
            sides = [4-d for _, d in G.degree(r)]
        else:
            sides = [4-d for _, d in G.degree(r)]
        perimeter = sum(sides)
        price += area * perimeter
    return price


if __name__ == "__main__":
    use_example = "--example" in sys.argv
    garden = parse_input(use_example)
    result_1 = solve_1_2(garden, bulk_discount=False)
    print(f'Result 1: {result_1}')
    result_2 = solve_1_2(garden, bulk_discount=True)
    print(f'Result 2: {result_2}')
