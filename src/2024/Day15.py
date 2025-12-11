from __future__ import annotations
from typing import Union

from Day import Day
from Map import Map
from Warehouse import (Robot, Box, Wall, Space)


class Day15(Day):

    def __init__(self,
                 auto_fetch: bool = True,
                 auto_parse: bool = True) -> None:
        super().__init__(year='2024', day='15', auto_fetch=auto_fetch, auto_parse=auto_parse)

    def parse_puzzle(self) -> None:
        self.puzzle_raw = self.puzzle_raw.strip()
        wh_str, dirseq = self.puzzle_raw.split('\n\n')
        dirseq = dirseq.replace('\n', '')
        warehouse_map = Map(wh_str, str)
        self.puzzle = {
            'map': warehouse_map,
            'dirseq': dirseq
        }

    def is_robot(self, object_: object) -> bool:
        return type(object_) == Robot  # noqa: E721

    def is_box(self, object_: object) -> bool:
        return type(object_) == Box  # noqa: E721

    def is_left_box(self, object_: object) -> bool:
        return type(object_) == Box and object_.is_left_half  # noqa: E721

    def build_warehouse(self, expand: bool = False) -> Map:
        assert isinstance(self.puzzle['map'], Map)
        # Allocate the warehouse with the proper dimensions
        height = self.puzzle['map'].x_max+1
        if expand:
            width = 2*(self.puzzle['map'].y_max+1)
        else:
            width = self.puzzle['map'].y_max+1
        warehouse: list[list[Union[Robot, Wall, Space, Box, Box, None]]] = [
            [None for _ in range(width)] for _ in range(height)
        ]
        # Build a warehouse of objects based on the map
        for p, e in self.puzzle['map'].enumerate_map():
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

    def solve_part_1(self, expand=False) -> int:
        warehouse = self.build_warehouse(expand=expand)
        robot = warehouse.get_first_element_by_condition(self.is_robot)
        assert isinstance(self.puzzle['dirseq'], str)
        for d in self.puzzle['dirseq']:
            robot.push(d)
        box = self.is_left_box if expand else self.is_box
        gps = [100*e.x + e.y for e in warehouse.find_all_elements_by_condition(box)]
        return sum(gps)

    def solve_part_2(self, expand=True) -> int:
        return self.solve_part_1(expand=expand)


def main() -> dict[str, int]:  # pragma: no cover
    today = Day15()
    today.solve()
    return today.answer


if __name__ == "__main__":  # pragma: no cover
    answer = main()
    print(f'Part 1: {answer['part_1']}')
    print(f'Part 2: {answer['part_2']}')
