import sys
import networkx as nx

import InputFetcher
from Coordinate import Coordinate

EXAMPLE = """\
5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0\
"""


def parse_input(example: bool) -> list[Coordinate]:
    data = EXAMPLE if example else InputFetcher.fetch_input('2024', '18')
    data = data.strip()
    y_x = [c.split(',') for c in data.split('\n')]
    x_y = [Coordinate(int(x), int(y)) for y, x in y_x]
    return x_y


def build_graph(ram_size: int,
                bytz: list[Coordinate]) -> nx.Graph:
    xy_max = ram_size-1
    R = nx.Graph()
    for x in range(xy_max+1):
        for y in range(xy_max+1):
            node = Coordinate(x, y)
            if node not in bytz:
                R.add_node(node)
                # Note: not the most efficient as it will add every edge twice (once from both directions)
                [R.add_edge(node, n, weight=1) for n in node.get_neighbors(xy_max, xy_max) if n not in bytz]
    return R


def solve_1(ram_size: int,
            bytz: list[Coordinate]) -> int:
    R = build_graph(ram_size, bytz)
    source = Coordinate(0, 0)
    target = Coordinate(ram_size-1, ram_size-1)
    return nx.shortest_path_length(R, source, target)


def solve_2(ram_size: int,
            bytz: list[Coordinate]) -> str:
    R = build_graph(ram_size, [])
    source = Coordinate(0, 0)
    target = Coordinate(ram_size-1, ram_size-1)
    for b in bytz:
        R.remove_node(b)
        if not nx.has_path(R, source, target):
            break
    return ','.join(map(str, [b.y, b.x]))


if __name__ == "__main__":
    use_example = "--example" in sys.argv
    bytz = parse_input(use_example)
    if use_example:
        ram_size = 7
        byte_num = 12
    else:
        ram_size = 71
        byte_num = 1024
    result_1 = solve_1(ram_size, bytz[:byte_num])
    if use_example:
        assert result_1 == 22, result_1
    print(f'Result 1: {result_1}')
    result_2 = solve_2(ram_size, bytz)
    if use_example:
        assert result_2 == '6,1', result_2
    print(f'Result 2: {result_2}')
