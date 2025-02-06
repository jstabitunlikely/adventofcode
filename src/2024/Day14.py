import re
from functools import reduce
from operator import mul

from Day import Day
from Coordinate import Coordinate


class Day14(Day):

    def __init__(self,
                 auto_fetch: bool = True,
                 auto_parse: bool = True) -> None:
        super().__init__(year='2024', day='14', auto_fetch=auto_fetch, auto_parse=auto_parse)

    def parse_puzzle(self) -> None:
        self.puzzle_raw = self.puzzle_raw.strip()
        puzzle_raw_split = self.puzzle_raw.split('\n')
        numbers_re = re.compile(r'[0-9-]+', flags=re.DOTALL)
        robots = []
        for px, py, vx, vy in [re.findall(numbers_re, m) for m in puzzle_raw_split]:
            p = Coordinate(int(px), int(py))
            v = Coordinate(int(vx), int(vy))
            robots.append((p, v))
        self.puzzle = robots

    def draw(self,
             robots: list[Coordinate],
             width: int,
             height: int):
        # Note: swapping x-y for proper visualization
        M = [['.'] * width for _ in range(height)]
        for r in robots:
            M[r.y][r.x] = '*'
        for row in M:
            print(''.join(row))

    def solve_part_1(self,
                     width: int = 101,
                     height: int = 103,
                     ticks: int = 100) -> int:
        # Advance the robots for the given number of ticks
        robots_advanced = [
            Coordinate(
                (p.x + v.x * ticks) % width,
                (p.y + v.y * ticks) % height
            ) for p, v in self.puzzle
        ]
        # Count the number of robots in each quadrant
        hw = width//2
        hh = height//2
        rpq = [
            [r for r in robots_advanced if r.x > hw and r.y < hh],
            [r for r in robots_advanced if r.x < hw and r.y < hh],
            [r for r in robots_advanced if r.x > hw and r.y > hh],
            [r for r in robots_advanced if r.x < hw and r.y > hh],
        ]
        return reduce(mul, map(len, rpq))

    def solve_part_2(self,
                     width: int = 101,
                     height: int = 103) -> int:
        position, velocity = zip(*self.puzzle)
        robots_p = list(position)
        robots_v = list(velocity)
        WINDOW = 50
        THRESHOLD = 0.50 * len(self.puzzle)
        tick = 1
        while True:
            robots_p = [
                Coordinate(
                    (p.x + robots_v[j].x) % width,
                    (p.y + robots_v[j].y) % height
                ) for j, p in enumerate(robots_p)
            ]
            for x in range(height-WINDOW):
                q = [r for r in robots_p if x <= r.x <= x+WINDOW and x <= r.y <= x+WINDOW]
                if len(q) > THRESHOLD:
                    # self.draw(robots_p, width, height)
                    break
            else:
                tick += 1
                continue
            break
        return tick


def main() -> dict[str, str]:  # pragma: no cover
    today = Day14()
    today.solve()
    return today.answer


if __name__ == "__main__":  # pragma: no cover
    answer = main()
    print(f'Part 1: {answer['part_1']}')
    print(f'Part 2: {answer['part_2']}')
