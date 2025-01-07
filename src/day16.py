import sys
import networkx as nx

import inputfetcher
from inputparsers import parse_matrix2d
from Coordinate import Coordinate

EXAMPLE = """\
###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############\
"""

EXAMPLE = """\
#################
#...#...#...#..E#
#.#.#.#.#.#.#.#.#
#.#.#.#...#...#.#
#.#.#.#.###.#.#.#
#...#.#.#.....#.#
#.#.#.#.#.#####.#
#.#...#.#.#.....#
#.#.#####.#.###.#
#.#.#.......#...#
#.#.###.#####.###
#.#.#...#.....#.#
#.#.#.#####.###.#
#.#.#.........#.#
#.#.#.#########.#
#S#.............#
#################\
"""


def parse_input(example: bool) -> list[list[str]]:
    data = EXAMPLE if example else inputfetcher.fetch_input('2024', '16')
    return parse_matrix2d(data, str)


def build_maze_graph(maze: list[list[str]]) -> tuple[nx.Graph, Coordinate, Coordinate]:
    maze_graph = nx.Graph()
    start = (-1, -1)
    end = (-1, -1)
    for i, row in enumerate(maze):
        for j, e in enumerate(row):
            if e not in '.ES':
                continue
            p = Coordinate(i, j)
            maze_graph.add_node(p)
            if e == 'E':
                end = p
            elif e == 'S':
                start = p
            neighbors = [np for np in p.get_neighbor_coordinates()]
            for e in neighbors:
                if maze[e.x][e.y] in '.ES':
                    maze_graph.add_edge(p, e)
    return maze_graph, start, end


def solve_1(maze: list[list[str]]) -> int:
    maze_graph, start, end = build_maze_graph(maze)
    all_paths = nx.all_simple_paths(maze_graph, start, end)
    min_score = float('inf')
    for path in all_paths:
        score = 0
        # As per spec, deers are facing East at the start
        dirvector = Coordinate(0, 1)
        for node_1, node_2 in zip(path, path[1:]):
            score += 1
            dirvector_next = node_2 - node_1
            if dirvector_next != dirvector:
                score += 1000
            dirvector = dirvector_next
        min_score = min(min_score, score)
    return min_score


if __name__ == "__main__":
    use_example = "--example" in sys.argv
    maze = parse_input(use_example)
    result_1 = solve_1(maze)
    print(f'Result 1: {result_1}')
