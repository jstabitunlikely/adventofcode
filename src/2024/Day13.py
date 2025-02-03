import re
import numpy as np
from scipy import linalg

from Day import Day
from utils import is_int


class Day13(Day):

    def __init__(self,
                 auto_fetch: bool = True,
                 auto_parse: bool = True) -> None:
        super().__init__(year='2024', day='13', auto_fetch=auto_fetch, auto_parse=auto_parse)
        self.CORRECTION = 10_000_000_000_000
        # REVISIT: how to find the right value for REL_TOL?
        # 1e-14 is an arbitrary value, but it works for the input
        self.REL_TOL = 1e-14

    def parse_puzzle(self) -> None:
        puzzle_raw = self.puzzle_raw.split('\n\n')
        numbers_re = re.compile(r'\d+', flags=re.DOTALL)
        machines = []
        for ax, ay, bx, by, px, py in [re.findall(numbers_re, m) for m in puzzle_raw]:
            a = np.array([[ax, bx], [ay, by]], dtype=int)
            b = np.array([px, py], dtype=int)
            machines.append([a, b])
        self.puzzle = machines

    def solve_part_1(self, correction: bool = False):
        if correction:
            self.puzzle = [[a, [bx+self.CORRECTION, by+self.CORRECTION]] for a, [bx, by] in self.puzzle]
        cost = [3, 1]
        tokens = 0
        for [a, b] in self.puzzle:
            x = linalg.solve(a, b, check_finite=False)
            # No solution at all
            if not len(x):
                continue
            # No solution over integers
            if not all([is_int(n, self.REL_TOL) for n in x]):
                continue
            tokens += np.dot(cost, x)
        return int(tokens)

    def solve_part_2(self):
        return self.solve_part_1(correction=True)


def main() -> dict[str, str]:  # pragma: no cover
    today = Day13()
    today.solve()
    return today.answer


if __name__ == "__main__":  # pragma: no cover
    answer = main()
    print(f'Part 1: {answer['part_1']}')
    print(f'Part 2: {answer['part_2']}')
