import sys
import networkx as nx

import inputfetcher
from Map import Map

EXAMPLE = """\
###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############\
"""


def parse_input(example: bool) -> Map:
    data = EXAMPLE if example else inputfetcher.fetch_input('2024', '20')
    return Map(data, str)


def build_graph(racetrack: Map) -> dict:
    results = {
        'graph': nx.Graph(),
        'tunnels': [],
    }
    for p, tile in racetrack.enumerate_coordinates():
        if tile == '#':
            continue
        # Add non-wall tiles as nodes
        results['graph'].add_node(p)
        # Add edges between non-wall tiles
        neighbors = racetrack.get_neighbors(coordinate=p, direction="^>v<", distance=1)
        for n in [c for c, t in neighbors if t in '.SE']:
            results['graph'].add_edge(p, n)

        # Find potential tunnels

        # Part 1
        neighbors = racetrack.get_neighbors_by_direction(coordinate=p, direction="^>v<", distance=2)
        for _, n in neighbors.items():
            # Second and/or first neighbor is already outside the map
            if len(n) != 2:
                continue
            # First neighbor is a wall, second one is a race track again
            # Note: n[x][0] is the coordinate, n[x][1] is the tile value
            # REVISIT: a more readable abstraction instead of a simple tuple
            elif n[0][1] == '#' and n[1][1] in '.SE':
                # Every tunnel is discovered twice (from both ends), so filter it
                if (n[1][0], p) not in results['tunnels']:
                    results['tunnels'].append((p, n[1][0]))

        # Part 2 needs a more sophisticated way to find the end of the tunnel
        # TODO

    return results


def solve_1_2(racetrack: Map,
              time_limit: int,
              use_example: bool = False) -> int:
    R = build_graph(racetrack)
    cheats = [nx.shortest_path_length(R['graph'], t[0], t[1]) - 2 for t in R['tunnels']]
    if use_example:
        return sum(cheats)
    return len([c for c in cheats if c >= 100])


if __name__ == "__main__":
    use_example = "--example" in sys.argv
    racetrack = parse_input(use_example)
    result_1 = solve_1_2(racetrack, 2, use_example)
    if use_example:
        # The example gives a trivial 0 to the actual question,
        # so using the sum of all possible cheated picoseconds
        assert result_1 == 382, f'Total cheats is {result_1}'
    print(f'Result 1: {result_1}')
    result_2 = solve_1_2(racetrack, 20, use_example)
    if use_example:
        # The example gives a trivial 0 to the actual question,
        # so using the sum of all possible cheated picoseconds
        assert result_2 == 16940, f'Total cheats is {result_2}'
    print(f'Result 2: {result_2}')
