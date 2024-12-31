import sys
import inputfetcher

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

DIRECTION = "^>v<"

DIR_MAP = {
    "^": (-1, 0),
    ">": (0, 1),
    "v": (1, 0),
    "<": (0, -1),
}


def parse_input(use_example: bool):
    data = EXAMPLE if use_example else inputfetcher.fetch_input('2024', '6')
    return [list(line) for line in data.split()]


def is_on_map(px: int,
              py: int) -> bool:
    if px not in range(len(lab_map)):
        return False
    elif py not in range(len(lab_map[0])):
        return False
    else:
        return True


def turn_right(dir: int) -> int:
    return (dir + 1) % 4


def step(dir: int,
         px: int,
         py: int) -> tuple[int, int]:
    px_next = px + DIR_MAP[DIRECTION[dir]][0]
    py_next = py + DIR_MAP[DIRECTION[dir]][1]
    return (px_next, py_next)


def is_obstacle(px: int,
                py: int,
                lab_map: list[list]) -> bool:
    if is_on_map(px, py):
        return lab_map[px][py] == "#"


def find_guard(lab_map: list[list]):
    for x, row in enumerate(lab_map):
        for y, e in enumerate(row):
            if e in ["^", ">", "v", "<"]:
                return (DIRECTION.index(e), x, y)


def walk(guard: tuple[int, int, int],
         lab_map: list[list]) -> tuple[set[tuple[int, int]], bool]:
    dir, px, py = guard
    # Unique positions visited
    visited = set([(px, py)])
    # Path history with directions
    path = set([guard])
    loop = False
    while True:
        # Look ahead
        px_next, py_next = step(dir, px, py)
        # Check if we're at the edge of the map
        if not is_on_map(px_next, py_next):
            break
        # Check if there's an obstacle ahead
        while is_obstacle(px_next, py_next, lab_map):
            dir = turn_right(dir)
            px_next, py_next = step(dir, px, py)
        # Check if we're running in circles (for Part 2 only)
        if (dir, px_next, py_next) in path:
            loop = True
            break
        # Actually step ahead
        px, py = px_next, py_next
        # Save current position
        visited.add((px, py))
        path.add((dir, px, py))
    return visited, loop


def solve_1_2(lab_map: list[list]) -> int:
    guard = find_guard(lab_map)
    visited, _ = walk(guard, lab_map)
    num_visited = len(visited)
    # As per spec, we can't put an obstacle on the guard's starting position
    visited.remove((guard[1], guard[2]))
    loops = 0
    # Try putting an obstacle onto each visited position (temporarily) and
    # do the walk again, checking if the new path has a loop
    for (px, py) in visited:
        lab_map[px][py] = "#"
        _, loop = walk(guard, lab_map)
        loops += 1 if loop else 0
        lab_map[px][py] = "."
    return num_visited, loops


if __name__ == "__main__":
    use_example = "--example" in sys.argv
    lab_map = parse_input(use_example)
    result_1, result_2 = solve_1_2(lab_map)
    print(f'Result 1: {result_1}')
    print(f'Result 2: {result_2}')
