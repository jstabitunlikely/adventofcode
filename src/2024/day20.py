import sys

import InputFetcher
from Map import Map
from Coordinate import Coordinate

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
    data = EXAMPLE if example else InputFetcher.fetch_input('2024', '20')
    return Map(data, str)


def get_track(racetrack: Map,
              start: Coordinate,
              end: Coordinate) -> list[Coordinate]:
    track = [start]
    pp = start
    p = start
    while p != end:
        pn = [n[0] for n in racetrack.get_neighbors(p, '^>v<') if n[1] in '.SE' and n[0] != pp][0]
        track.append(pn)
        pp = p
        p = pn
    return track


def solve_1_2(racetrack: Map,
              cheat_max: int,
              limit: int) -> int:
    endpoints = racetrack.find_first_elements(['S', 'E'])
    track = get_track(racetrack, endpoints['S'], endpoints['E'])
    cheats = []
    # track_len = len(track)
    for i, p1 in enumerate(track[:-1]):
        # REVISIT: runtime is ~3m
        # if not i % (track_len//100+1):
        #     print(f'.', end='')
        p2s = [p2 for p2 in track[i+1:] if 0 < racetrack.get_distance(p1, p2) <= cheat_max]
        cheat = [track[i:].index(p2) - racetrack.get_distance(p1, p2) for p2 in p2s]
        cheat = [c for c in cheat if c > 0]
        cheats.extend(cheat)
    return len([c for c in cheats if c >= limit])


if __name__ == "__main__":
    use_example = "--example" in sys.argv
    racetrack = parse_input(use_example)
    limit = 0 if use_example else 100
    result_1 = solve_1_2(racetrack, 2, limit)
    if use_example:
        assert result_1 == 44, result_1
    print(f'Result 1: {result_1}')
    limit = 50 if use_example else 100
    result_2 = solve_1_2(racetrack, 20, limit)
    if use_example:
        assert result_2 == 285, result_2
    print(f'Result 2: {result_2}')
