from Day import Day
from Coordinate import Coordinate
from itertools import combinations
from functools import cache

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

    @cache
    def is_outside_shape(self, c: Coordinate) -> bool:
        if c in self.shape:
            return False

        to_left = [e for e in self.shape if e.y == c.y and e.x < c.x]
        if not to_left:
            return True

        # Merge consecutive elements in to_left
        to_left_reduced = [e for e in to_left if Coordinate(e.x+1, e.y) not in to_left]
        if len(to_left_reduced) % 2:
            return False

        return True

    def generate_shape(self) -> None:
        shape = []
        for red1, red2 in zip(self.puzzle, [self.puzzle[-1]] + self.puzzle[:-1]):
            x_min = min(red1.x, red2.x)
            x_max = max(red1.x, red2.x)
            y_min = min(red1.y, red2.y)
            y_max = max(red1.y, red2.y)
            for x in range(x_min, x_max+1):
                for y in range(y_min, y_max+1):
                    shape.append(Coordinate(x, y))
        self.shape = tuple(set(shape))

    def solve_part_1(self) -> dict[str, int]:
        # Part 1
        rectangles = list(combinations(self.puzzle, 2))
        area_max = 0
        # Part 2
        self.generate_shape()
        area_max_inside_only = 0
        for r in rectangles:
            # Part 1
            diff = abs(r[0] - r[1])
            area = (diff.x+1) * (diff.y+1)
            area_max = max(area, area_max)
            # Part 2
            if self.is_outside_shape(Coordinate(r[0].x, r[1].y)):
                continue
            if self.is_outside_shape(Coordinate(r[1].x, r[0].y)):
                continue
            area_max_inside_only = max(area, area_max_inside_only)

        return {
            'part_1': area_max,
            'part_2': area_max_inside_only
        }

    solve_part_2 = solve_part_1


def main() -> dict[str, int]:  # pragma: no cover
    today = y25d09()
    today.solve()
    return today.answer


if __name__ == "__main__":  # pragma: no cover
    answer = main()
    print(f'Part 1: {answer['part_1']}')
    print(f'Part 2: {answer['part_2']}')
