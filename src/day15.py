import sys
from functools import reduce

import inputfetcher
from Coordinate import Coordinate

EXAMPLE = """\
##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^\
"""

MINI_EXAMPLE = """\
########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

<^^>>>vv<v>>v<<\
"""


class WarehouseElement(Coordinate):

    DIRMAP = {
        "^": (-1, 0),
        ">": (0, 1),
        "v": (1, 0),
        "<": (0, -1),
    }

    def __init__(self,
                 x: int,
                 y: int,
                 warehouse: list[list]):
        super().__init__(x, y)
        self.warehouse = warehouse


class Wall(WarehouseElement):

    def push(self, dir: str) -> tuple[int, int]:
        return (self.x, self.y)

    def __repr__(self):
        return repr('#')


class Space(WarehouseElement):

    def push(self, dir: str) -> tuple[int, int]:
        return (-1, -1)

    def __repr__(self):
        return repr('.')


class Box(WarehouseElement):

    def __init__(self,
                 x: int,
                 y: int,
                 warehouse: list[list]):
        super().__init__(x, y, warehouse)
        self.gps = 100*x + y

    def push(self, dir: str) -> tuple[int, int]:
        nx = self.x + self.DIRMAP[dir][0]
        ny = self.y + self.DIRMAP[dir][1]
        if self.warehouse[nx][ny].push(dir) != (nx, ny):
            self.warehouse[nx][ny] = self
            self.warehouse[self.x][self.y] = Space(self.x, self.y, self.warehouse)
            self.x = nx
            self.y = ny
            return (nx, ny)
        else:
            return (self.x, self.y)

    def __repr__(self):
        return repr('O')


class Robot(Box):

    def __repr__(self):
        return repr('@')


def parse_input(example: bool) -> tuple[list[list], str]:
    data = EXAMPLE if example else inputfetcher.fetch_input('2024', '15')
    data = data.strip()
    wh_str, dirseq = data.split('\n\n')
    wh_str = wh_str.split('\n')
    dirseq = dirseq.replace('\n', '')
    # Fill an empty warehouse
    warehouse = [[None for _ in range(len(wh_str[0]))] for _ in range(len(wh_str))]
    for x, row in enumerate(wh_str):
        for y, c in enumerate(row):
            if c == '@':
                warehouse[x][y] = Robot(x, y, warehouse)
            elif c == '#':
                warehouse[x][y] = Wall(x, y, warehouse)
            elif c == '.':
                warehouse[x][y] = Space(x, y, warehouse)
            elif c == 'O':
                warehouse[x][y] = Box(x, y, warehouse)
    return warehouse, dirseq


def solve_1(warehouse: list[list],
            dirseq: str) -> int:
    # Find the robot
    rx, ry = [[e.x, e.y] for row in warehouse for e in row if type(e) == Robot][0]
    # Push it around
    for d in dirseq:
        rx, ry = warehouse[rx][ry].push(d)
    # Calculate GPS values
    gps = [100*e.x + e.y for row in warehouse for e in row if type(e) == Box]
    return sum(gps)


def solve_2() -> int:
    return 0


if __name__ == "__main__":
    use_example = "--example" in sys.argv
    warehouse, dirseq = parse_input(use_example)
    result_1 = solve_1(warehouse, dirseq)
    print(f'Result 1: {result_1}')
    result_2 = solve_2()
    print(f'Result 2: {result_2}')
