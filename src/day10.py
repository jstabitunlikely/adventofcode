import sys

import inputfetcher
from Map import Map
from Coordinate import Coordinate


EXAMPLE = """\
89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732\
"""


def parse_input(example: bool) -> list[list[int]]:
    data = EXAMPLE if example else inputfetcher.fetch_input('2024', '10')
    return Map(data, int).map_


def frame_map(map_: list[list[int]]) -> list[list[int]]:
    """
    Frame the map with -1s to handle out-of-bounds errors with the core algorithm.
    """
    w = len(map_[0])
    f = -1
    map_ = [[f]*w] + map_ + [[f]*w]
    map_ = [[f] + row + [f] for row in map_]
    return map_


def find_trailheads(map_: list[list[int]]) -> list[Coordinate]:
    return [Coordinate(x, y) for x in range(len(map_)) for y in range(len(map_[0])) if map_[x][y] == 0]


def get_height(position: Coordinate, map_: list[list[int]]) -> int:
    return map_[position.x][position.y]


def hike(position: Coordinate, map_: list[list[int]]) -> list[Coordinate]:
    peaks = []
    for dir in [Coordinate(0, -1), Coordinate(0, 1), Coordinate(-1, 0), Coordinate(1, 0)]:
        position_next = position + dir
        height = get_height(position, map_)
        height_next = get_height(position_next, map_)
        # Stay on the trail
        if height_next == height + 1:
            # Arrived at the peak
            if height_next == 9:
                peaks += [position_next]
            # Continue the hike
            else:
                peaks += hike(position_next, map_)
    return peaks


def solve_1_2(map_: list[list[int]]) -> tuple[int, int]:
    trailheads = find_trailheads(map_)
    scores = 0
    ratings = 0
    for th in trailheads:
        peaks = hike(th, map_)
        scores += len(set(peaks))
        ratings += len(peaks)
    return (scores, ratings)


if __name__ == "__main__":
    use_example = "--example" in sys.argv
    map_ = parse_input(use_example)
    map_ = frame_map(map_)
    result_1, result_2 = solve_1_2(map_)
    if use_example:
        assert result_1 == 36, result_1
        assert result_2 == 81, result_2
    print(f'Result 1: {result_1}')
    print(f'Result 2: {result_2}')
