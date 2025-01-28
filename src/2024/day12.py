import sys
import networkx as nx

import inputfetcher
from Map import Map
from Coordinate import Coordinate

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


def parse_input(example: bool) -> Map:
    data = EXAMPLE if example else inputfetcher.fetch_input('2024', '12')
    return Map(data, str)


def get_sides(p: Coordinate,
              garden: Map) -> list[bool]:
    plot_p = garden.get_element(p)
    sides = []
    for n, plot_n in garden.get_neighbors(p, "^>v<", check_edges=False):
        if garden.has_coordinate(n):
            sides.append(plot_n != plot_p)
        else:
            sides.append(True)
    return sides


def build_graph(garden: Map,
                bulk_discount: bool = False) -> nx.Graph:
    G = nx.Graph()
    for p, plot1 in garden.enumerate_map():
        G.add_node(p)
        for n, plot2 in garden.get_neighbors(p, "^>v<"):
            if plot1 == plot2:
                d = 0
                if bulk_discount:
                    # REVISIT: I feel like this spoils the elegance of the graph approach.
                    sides_p = get_sides(p, garden)
                    sides_n = get_sides(n, garden)
                    d = sum([a & b for (a, b) in zip(sides_p, sides_n)])
                G.add_edge(p, n, discount=d)
    return G


def solve_1_2(garden: Map,
              bulk_discount: bool = False) -> int:
    G = build_graph(garden, bulk_discount)
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
