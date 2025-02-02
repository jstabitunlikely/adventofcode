from __future__ import annotations
from typing import Union

import sys

import InputFetcher
from Warehouse import (Robot, Box, Wall, Space)
from Map import Map

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


def is_robot(object_: object) -> bool:
    return type(object_) == Robot  # noqa: E721


def is_box(object_: object) -> bool:
    return type(object_) == Box  # noqa: E721


def is_left_box(object_: object) -> bool:
    return type(object_) == Box and object_.is_left_half  # noqa: E721


def parse_input(example: bool) -> tuple[Map, str]:
    data = EXAMPLE if example else InputFetcher.fetch_input('2024', '15')
    data = data.strip()
    wh_str, dirseq = data.split('\n\n')
    dirseq = dirseq.replace('\n', '')
    warehouse_map = Map(wh_str, str)
    return warehouse_map, dirseq


def build_warehouse(warehouse_map: Map,
                    expand: bool = False) -> Map:
    # Allocate the warehouse with the proper dimensions
    height = warehouse_map.x_max+1
    if expand:
        width = 2*(warehouse_map.y_max+1)
    else:
        width = warehouse_map.y_max+1
    warehouse: list[list[Union[Robot, Wall, Space, Box, Box, None]]] = [
        [None for _ in range(width)] for _ in range(height)
    ]
    # Build a warehouse of objects based on the map
    for p, e in warehouse_map.enumerate_map():
        x = p.x
        if expand:
            y1 = 2*p.y
            y2 = 2*p.y + 1
        else:
            y1 = p.y
        match e:
            case '#':
                warehouse[x][y1] = Wall(x, y1)
                if expand:
                    warehouse[x][y2] = Wall(x, y2)
            case '.':
                warehouse[x][y1] = Space(x, y1)
                if expand:
                    warehouse[x][y2] = Space(x, y2)
            case 'O':
                if expand:
                    left_box = Box(x, y1, is_left_half=True, warehouse=warehouse)
                    right_box = Box(x, y2, is_left_half=False, warehouse=warehouse)
                    left_box.other_half = right_box
                    right_box.other_half = left_box
                    warehouse[x][y1] = left_box
                    warehouse[x][y2] = right_box
                else:
                    warehouse[x][y1] = Box(p.x, p.y, is_left_half=False, warehouse=warehouse)
            case '@':
                warehouse[x][y1] = Robot(x, y1, warehouse)
                if expand:
                    warehouse[x][y2] = Space(x, y2)
    return Map(warehouse, object)


def solve_1(warehouse_map: Map,
            dirseq: str) -> int:
    warehouse = build_warehouse(warehouse_map)
    robot = warehouse.get_first_element_by_condition(is_robot)
    for d in dirseq:
        robot.push(d)
    gps = [100*e.x + e.y for e in warehouse.find_all_elements_by_condition(is_box)]
    return sum(gps)


def solve_2(warehouse_map: Map,
            dirseq: str) -> int:
    warehouse = build_warehouse(warehouse_map, expand=True)
    robot = warehouse.get_first_element_by_condition(is_robot)
    for d in dirseq:
        robot.push(d)
    gps = [100*e.x + e.y for e in warehouse.find_all_elements_by_condition(is_left_box)]
    return sum(gps)


if __name__ == "__main__":
    use_example = "--example" in sys.argv
    warehouse, dirseq = parse_input(use_example)
    result_1 = solve_1(warehouse, dirseq)
    if use_example:
        assert result_1 == 10092, result_1
    print(f'Result 1: {result_1}')
    result_2 = solve_2(warehouse, dirseq)
    if use_example:
        assert result_2 == 9021, result_2
    print(f'Result 2: {result_2}')
