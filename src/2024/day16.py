import sys
import networkx as nx

import inputfetcher
from Map import Map
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


def parse_input(example: bool) -> Map:
    data = EXAMPLE if example else inputfetcher.fetch_input('2024', '16')
    return Map(data, str)


def build_maze_graph(maze: Map) -> nx.Graph:
    M = nx.Graph()
    for p, p_tile in maze.enumerate_map():
        # Add non-wall positions as nodes
        if p_tile == '#':
            continue
        M.add_node(p)
        # Add edges between non-wall nodes
        # Note: not the most efficient as it will add every edge twice (once from both directions)
        for n, n_tile in maze.get_neighbors(p, '^>v<'):
            if n_tile != '#':
                M.add_edge(p, n)
        # Additional virtual nodes for the nodes before start/after end positions,
        #   so the line graph will have an entry and (two possible) exit points.
        # Note: assuming S/E are always in the bottom-left/top-right corners
        if p_tile == 'S':
            # One node is enough, because deers are always facing East at Start
            s = p + maze.COMPASS['<']
            M.add_node(s)
            M.add_edge(s, p)
        elif p_tile == 'E':
            # Two nodes, because we can arrive from two directions
            e1 = p + maze.COMPASS['>']
            e2 = p + maze.COMPASS['^']
            M.add_node(e1)
            M.add_node(e2)
            M.add_edge(e1, p)
            M.add_edge(e2, p)
    return M


def assign_weights(Mp: nx.Graph,
                   step: int = 1,
                   turn: int = 1000):
    turn_step = turn + step
    # Assigning the 'cost' of the moves to the edges as weights
    for n1, n2 in Mp.edges():
        # An edge of M' describes a step in M, while also 'remembering' the previous step.
        # Its two nodes, n1 and n2 denote node pairs in M e.g., (u, v) and (v, w).
        # Coming from u, stepping from v to w. We just have to check if the direction has changed between:
        #   - direction of the previous step: v-u
        #   - direction of the current step: w-u
        # Since it's not a directed graph, (u,v) can be either (n1[0],n1[1]) or (n1[1],n1[0]).
        #   Same goes for (v,w) and n2. Using the absolute difference to handle this.
        dirvector_n1 = abs(n1[1] - n1[0])
        dirvector_n2 = abs(n2[1] - n2[0])
        if dirvector_n1 == dirvector_n2:
            Mp[n1][n2]['weight'] = step
        else:
            # Note: there's no turn in itself, it's a turn-and-step
            Mp[n1][n2]['weight'] = turn_step
    return Mp


def solve_1_2(maze: Map) -> tuple[int, int]:
    # Let's create a graph M from the maze:
    #   - nodes: non-wall tiles of the maze e.g., u = (x1,y1), v = (x2,y2)
    #   - edges: interpreted as 'steps in the maze'
    M = build_maze_graph(maze)
    # To find the shortest S-E path, we need to assign weights (cost of taking that step) to the edges first.
    # However, the weight depend on _how_ we got to a certain node. Let's create a
    # line graph M'=L(M) to handle this (source: https://en.wikipedia.org/wiki/Line_graph):
    #   - nodes: node pairs from M iff they have a common node e.g, ((u, v), (v, w))
    #   - edges: interpreted as 'we arrived to v from u, and now stepping from v to w'
    Mp = nx.line_graph(M)
    # Assigning the 'cost' of the moves to the edges as weights
    assign_weights(Mp)

    # Start/end nodes in the M' graph
    # Note: rather than finding S/E again,
    #   we assume they're always in the bottom-left/top-right corners.
    s = Coordinate(maze.x_max-1, 1)
    e = Coordinate(1, maze.y_max-1)
    assert maze.get_element(s) == 'S', 'Start position is not found at the expected place'
    assert maze.get_element(e) == 'E', 'End position is not found at the expected place'
    start = (s, s + maze.COMPASS['<'])
    # Note: There are two possible endings, because we can reach E from two directions
    end1 = (e, e + maze.COMPASS['>'])
    end2 = (e, e + maze.COMPASS['^'])

    # Find the shortest paths to both possible endings
    paths_to_end1 = list(nx.all_shortest_paths(Mp, start, end1, weight='weight'))
    paths_to_end2 = list(nx.all_shortest_paths(Mp, start, end2, weight='weight'))

    # Next, we have to decide which ending is better and work with that.
    #   Check which one has to shortest path to it.

    # The score is simply the sum of (edge) weights on the path.
    # Note: Need to subtract one because of the virtual nodes at the End
    min_score_to_end1 = min([nx.path_weight(Mp, path, 'weight') - 1 for path in paths_to_end1])
    min_score_to_end2 = min([nx.path_weight(Mp, path, 'weight') - 1 for path in paths_to_end2])
    if min_score_to_end1 < min_score_to_end2:
        min_score = int(min_score_to_end1)
        paths = paths_to_end1
    else:
        min_score = int(min_score_to_end2)
        paths = paths_to_end2

    # Get the number of unique positions in all the paths
    nodes = []
    # The nodes in M' are node pairs of M, flatten it
    list(nodes.extend(node) for path in paths for node in path)  # type: ignore[func-returns-value]
    # Need to subtract the virtual nodes we added when building the original graph
    num_unique_nodes = len(set(nodes)) - 2

    return min_score, num_unique_nodes


if __name__ == "__main__":
    use_example = "--example" in sys.argv
    maze = parse_input(use_example)
    result_1, result_2 = solve_1_2(maze)
    if use_example:
        assert result_1 == 11048, result_1
        assert result_2 == 64, result_2
    print(f'Result 1: {result_1}')
    print(f'Result 2: {result_2}')
