from __future__ import annotations
from typing import Optional, Union

import sys
from copy import deepcopy

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

    def nudge(self, dir: str) -> bool:
        return False

    def __repr__(self):
        return repr('#')


class Space(WarehouseElement):

    def push(self, dir: str) -> tuple[int, int]:
        return (-1, -1)

    def nudge(self, dir: str) -> bool:
        return True

    def __repr__(self):
        return repr('.')


class Box(WarehouseElement):

    def __init__(self,
                 x: int,
                 y: int,
                 warehouse: list[list]):
        super().__init__(x, y, warehouse)

    def push(self, dir: str) -> tuple[int, int]:
        nx = self.x + self.DIRMAP[dir][0]
        ny = self.y + self.DIRMAP[dir][1]
        # REVISIT: could use the nudge-push approach introduced for Part 2 for uniformity
        if self.warehouse[nx][ny].push(dir) != (nx, ny):
            self.warehouse[nx][ny] = self
            self.warehouse[self.x][self.y] = Space(self.x, self.y, self.warehouse)
            self.x = nx
            self.y = ny
        return (self.x, self.y)

    def __repr__(self):
        return repr('O')


class BigBox(Box):

    # REVISIT: could merge into Box while staying backward compatible with Part 1

    other_half: Optional[BigBox] = None

    def __init__(self,
                 x: int,
                 y: int,
                 is_left_half: bool,
                 warehouse: list[list]):
        super().__init__(x, y, warehouse)
        self.is_left_half = is_left_half

    # These flags prevent left and right halves infinitely nudging/pushing each other.
    is_nudge_in_progress = False
    is_push_in_progress = False

    def push(self, dir: str) -> tuple[int, int]:
        # Horizontal push is nothing special
        if dir in '<>':
            return super().push(dir)
        # Vertical push needs to handle both halves
        else:
            self.is_push_in_progress = True
            if self.nudge(dir):
                assert self.other_half is not None
                if not self.other_half.is_push_in_progress:
                    self.other_half.push(dir)
                super().push(dir)
            self.is_push_in_progress = False
            return (self.x, self.y)

    def nudge(self, dir: str) -> tuple[int, int]:
        self.is_nudge_in_progress = True
        nx = self.x + self.DIRMAP[dir][0]
        ny = self.y + self.DIRMAP[dir][1]
        ok = self.warehouse[nx][ny].nudge(dir)
        assert self.other_half is not None
        if not self.other_half.is_nudge_in_progress:
            ok &= self.other_half.nudge(dir)
        self.is_nudge_in_progress = False
        return ok

    def __repr__(self):
        if self.is_left_half:
            return repr('[')
        else:
            return repr(']')


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
    warehouse: list[list[Union[Robot, Wall, Space, Box, None]]] = [
        [None for _ in range(len(wh_str[0]))] for _ in range(len(wh_str))
    ]
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


def expand_warehouse(warehouse: list[list]) -> list[list]:
    warehouse_big: list[list[Union[Robot, Wall, Space, BigBox, None]]] = [
        [None for _ in range(2*len(warehouse[0]))] for _ in range(len(warehouse))
    ]
    for x, row in enumerate(warehouse):
        for y, c in enumerate(row):
            c_type = type(c)
            y1 = 2*y
            y2 = 2*y + 1
            if c_type == Robot:
                warehouse_big[x][y1] = Robot(x, y1, warehouse_big)
                warehouse_big[x][y2] = Space(x, y2, warehouse_big)
            elif c_type == Wall:
                warehouse_big[x][y1] = Wall(x, y1, warehouse_big)
                warehouse_big[x][y2] = Wall(x, y2, warehouse_big)
            elif c_type == Space:
                warehouse_big[x][y1] = Space(x, y1, warehouse_big)
                warehouse_big[x][y2] = Space(x, y2, warehouse_big)
            elif c_type == Box:
                warehouse_big[x][y1] = BigBox(x, y1, is_left_half=True, warehouse=warehouse_big)
                warehouse_big[x][y2] = BigBox(x, y2, is_left_half=False, warehouse=warehouse_big)
                # REVISIT how to type hint this
                warehouse_big[x][y1].other_half = warehouse_big[x][y2]  # type:ignore[union-attr]
                warehouse_big[x][y2].other_half = warehouse_big[x][y1]  # type:ignore[union-attr]
    return warehouse_big


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


def solve_2(warehouse: list[list],
            dirseq: str) -> int:
    # Find the robot
    rx, ry = [[e.x, e.y] for row in warehouse for e in row if type(e) == Robot][0]
    # Push it around
    for d in dirseq:
        rx, ry = warehouse[rx][ry].push(d)
    # Calculate GPS values
    gps = [100*e.x + e.y for row in warehouse for e in row if type(e) == BigBox and e.is_left_half]
    return sum(gps)


if __name__ == "__main__":
    use_example = "--example" in sys.argv
    warehouse, dirseq = parse_input(use_example)
    result_1 = solve_1(deepcopy(warehouse), dirseq)
    if use_example:
        assert result_1 == 10092, result_1
    print(f'Result 1: {result_1}')
    warehouse_2 = expand_warehouse(deepcopy(warehouse))
    result_2 = solve_2(warehouse_2, dirseq)
    if use_example:
        assert result_2 == 9021, result_2
    print(f'Result 2: {result_2}')
