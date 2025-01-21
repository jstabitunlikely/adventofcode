import sys

import inputfetcher
from Map import Map
from Coordinate import Coordinate

EXAMPLE = """\
....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...\
"""


def parse_input(use_example: bool):
    data = EXAMPLE if use_example else inputfetcher.fetch_input('2024', '6')
    return Map(data, str)


def turn_right(dir_: int) -> int:
    return (dir_ + 1) % 4


def walk(guard: dict[str, Coordinate],
         lab: Map) -> tuple[set[Coordinate], bool]:
    guard_ = list(guard.items())[0]
    # Position of the guard
    p = guard_[1]
    # Direction of the guard as an integer
    idir = p.DIRECTIONS.index(guard_[0])
    # Unique positions visited
    visited = set([p])
    # Path history with directions
    path = set([(idir, p)])
    loop = False
    while True:
        # Look ahead
        p_next = p.get_neighbor(idir)
        # Check if we're at the edge of the map
        if not lab.has_coordinate(p_next):
            break
        # Check if there's an obstacle ahead
        while lab.get_element(p_next) == '#':
            idir = turn_right(idir)
            p_next = p.get_neighbor(idir)
        # Check if we're running in circles (for Part 2 only)
        if (idir, p_next) in path:
            loop = True
            break
        # Actually step ahead
        p = p_next
        # Save current position
        visited.add(p)
        path.add((idir, p))
    return visited, loop


def solve_1_2(lab: Map) -> tuple[int, int]:
    guard = lab.find_elements(['^', '>', 'v', '<'])
    visited, _ = walk(guard, lab)
    num_visited = len(visited)
    # As per spec, we can't put an obstacle on the guard's starting position
    guard_pos = list(guard.items())[0][1]
    visited.remove(guard_pos)
    loops = 0
    # Try putting an obstacle onto each visited position (temporarily) and
    # do the walk again, checking if the new path has a loop
    for p in visited:
        lab.set_element(p, "#")
        _, loop = walk(guard, lab)
        loops += 1 if loop else 0
        lab.set_element(p, ".")
    return num_visited, loops


if __name__ == "__main__":
    use_example = "--example" in sys.argv
    lab = parse_input(use_example)
    result_1, result_2 = solve_1_2(lab)
    if use_example:
        assert result_1 == 41, result_1
        assert result_2 == 6, result_2
    print(f'Result 1: {result_1}')
    print(f'Result 2: {result_2}')
