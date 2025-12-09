from Day import Day
from Coordinate import Coordinate
from itertools import combinations


class y25d09(Day):

    def __init__(self,
                 auto_fetch: bool = True,
                 auto_parse: bool = True) -> None:
        super().__init__(year='2025', day='09', auto_fetch=auto_fetch, auto_parse=auto_parse)

    def parse_puzzle(self) -> None:
        super().parse_puzzle()
        red_tiles = self.puzzle_raw.split()
        self.puzzle = []
        for rt in red_tiles:
            coordinate = list(map(int, rt.split(',')))
            self.puzzle.append(Coordinate(coordinate[0], coordinate[1]))

    def solve_part_1(self) -> int:
        rectangles = list(combinations(self.puzzle, 2))
        area_max = 0
        for r in rectangles:
            diff = abs(r[0] - r[1])
            area = (diff.x+1) * (diff.y+1)
            area_max = max(area, area_max)
        return area_max

    def solve_part_2(self) -> int:
        return 0


def main() -> dict[str, str]:  # pragma: no cover
    today = y25d09()
    today.solve()
    return today.answer


if __name__ == "__main__":  # pragma: no cover
    answer = main()
    print(f'Part 1: {answer['part_1']}')
    print(f'Part 2: {answer['part_2']}')
