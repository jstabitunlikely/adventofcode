import sys
from typing import Any

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


def parse_input(example: bool) -> Map:
    data = EXAMPLE if example else inputfetcher.fetch_input('2024', '10')
    return Map(data, int)


def find_trailheads(map_: Map,
                    trailhead: int = 0) -> list[Coordinate]:
    return map_.find_all_element(trailhead)


def hike(position: Coordinate,
         map_: Map) -> list[Coordinate]:
    peaks = []
    for _, dir_ in map_.COMPASS.items():
        position_next = position + dir_
        height = map_.get_element(position)
        height_next = map_.get_element(position_next)
        # Stay on the trail
        if height_next == height + 1:
            # Arrived at the peak
            if height_next == 9:
                peaks += [position_next]
            # Continue the hike
            else:
                peaks += hike(position_next, map_)
    return peaks


def solve_1_2(map_: Map) -> tuple[int, int]:
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
    map_.frame(-1)
    result_1, result_2 = solve_1_2(map_)
    if use_example:
        assert result_1 == 36, result_1
        assert result_2 == 81, result_2
    print(f'Result 1: {result_1}')
    print(f'Result 2: {result_2}')
