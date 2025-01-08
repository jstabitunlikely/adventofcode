import sys
import networkx as nx
from itertools import chain

import inputfetcher
from inputparsers import parse_matrix2d
from Coordinate import Coordinate
from utils import is_on_map

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

# EXAMPLE = """\
# #################
# #...#...#...#..E#
# #.#.#.#.#.#.#.#.#
# #.#.#.#...#...#.#
# #.#.#.#.###.#.#.#
# #...#.#.#.....#.#
# #.#.#.#.#.#####.#
# #.#...#.#.#.....#
# #.#.#####.#.###.#
# #.#.#.......#...#
# #.#.###.#####.###
# #.#.#...#.....#.#
# #.#.#.#####.###.#
# #.#.#.........#.#
# #.#.#.#########.#
# #S#.............#
# #################\
# """


def parse_input(example: bool) -> list[list[str]]:
    data = EXAMPLE if example else inputfetcher.fetch_input('2024', '16')
    return parse_matrix2d(data, str)


def build_maze_graph(maze: list[list[str]]) -> tuple[nx.Graph, Coordinate, Coordinate]:
    maze_graph = nx.Graph()
    for i, row in enumerate(maze):
        for j, c in enumerate(row):
            # Add non-wall positions as nodes
            if c not in '.ES':
                continue
            node = Coordinate(i, j)
            maze_graph.add_node(node)
            # Add edges between non-wall nodes
            neighbors = [np for np in node.get_neighbor_coordinates() if is_on_map(np, maze)]
            for n in neighbors:
                if maze[n.x][n.y] in '.ES':
                    maze_graph.add_edge(node, n)
            # Additional virtual nodes for the nodes before start/after end positions,
            #   so the line graph will have an entry and (two possible) exit points
            if c == 'S':
                s = Coordinate(i, j-1)
                maze_graph.add_node(s)
                maze_graph.add_edge(s, node)
            elif c == 'E':
                e1 = Coordinate(i, j+1)
                e2 = Coordinate(i-1, j)
                maze_graph.add_node(e1)
                maze_graph.add_node(e2)
                maze_graph.add_edge(e1, node)
                maze_graph.add_edge(e2, node)
    return maze_graph


def solve_1(maze: list[list[str]]) -> int:
    # Create a graph from the maze:
    #   nodes: tiles of the maze
    #   edges: possible steps deers can take
    M = build_maze_graph(maze)
    # To find the shortest S-E path, we need to assign weights to the edges.
    # However, weights depend on _how_ we got to a certain node. Line graphs
    # can help with that (https://en.wikipedia.org/wiki/Line_graph).
    #   nodes: node pairs from the original graph e.g., (u,v) - (v,w)
    #   edges: loosely speaking, an u-v-w path in the original graph
    Mp = nx.line_graph(M)

    # Start/end nodes in the M' graph
    x_max = len(maze)-1
    y_max = len(maze[0])-1
    # Note: rather than finding S/E again,
    #   we assume they're always in the bottom-left/top-right corners.
    assert maze[x_max-1][1] == 'S', 'Start position is not found at the expected place'
    assert maze[1][y_max-1] == 'E', 'End position is not found at the expected place'
    start = (Coordinate(x_max-1, 1), Coordinate(x_max-1, 0))
    end1 = (Coordinate(1, y_max-1), Coordinate(0, y_max-1))
    end2 = (Coordinate(1, y_max-1), Coordinate(1, y_max))

    # Assign weights based on whether the direction vector has changed between two nodes in Mp
    for n1, n2 in Mp.edges():
        dirvector_n1 = abs(n1[1] - n1[0])
        dirvector_n2 = abs(n2[1] - n2[0])
        if dirvector_n1 == dirvector_n2:
            Mp[n1][n2]['weight'] = 1
        else:
            Mp[n1][n2]['weight'] = 1001

    # Find the shortest paths to both possible endings
    paths_to_end1 = nx.all_shortest_paths(Mp, start, end1, weight='weight')
    paths_to_end2 = nx.all_shortest_paths(Mp, start, end2, weight='weight')
    all_paths = chain(paths_to_end1, paths_to_end2)

    # The score is simply the sum weight of the path
    scores = [nx.path_weight(Mp, path, 'weight') - 1 for path in all_paths]

    return min(scores)


if __name__ == "__main__":
    use_example = "--example" in sys.argv
    maze = parse_input(use_example)
    result_1 = solve_1(maze)
    print(f'Result 1: {result_1}')
