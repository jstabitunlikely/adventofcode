from typing import Any
from Day import Day


class y25d05(Day):

    def __init__(self,
                 auto_fetch: bool = True,
                 auto_parse: bool = True) -> None:
        super().__init__(year='2025', day='05', auto_fetch=auto_fetch, auto_parse=auto_parse)

    def parse_puzzle(self) -> None:
        super().parse_puzzle()
        fresh, available = self.puzzle_raw.strip().split('\n\n')
        fresh_ranges = []
        for f in fresh.split('\n'):
            min, max = f.split('-')
            fresh_ranges.append([int(min), int(max)])
        available_list = []
        for a in available.split('\n'):
            available_list.append(int(a))
        self.puzzle: dict[str, list[Any]] = {'fresh': fresh_ranges,
                                             'available': available_list}
        self.puzzle['fresh'].sort(key=lambda item: item
                                  [0])

    def solve_part_1(self) -> int:
        fresh = 0
        for a in self.puzzle['available']:
            for f in self.puzzle['fresh']:
                if f[0] <= a <= f[1]:
                    fresh += 1
                    break
        return fresh

    def solve_part_2(self) -> int:
        fresh_total = 0
        # Remove any range that is a complete sub-range of its predecessor
        nof_ranges = len(self.puzzle['fresh'])
        to_remove = []
        for i in range(nof_ranges):
            if i < nof_ranges-1:
                if (self.puzzle['fresh'][i+1][1] <= self.puzzle['fresh'][i][1]):
                    to_remove.append(i+1)
        to_remove.reverse()
        for i in to_remove:
            self.puzzle['fresh'].pop(i)

        # Strip ranges, so they don't overlap with the next one
        nof_ranges = len(self.puzzle['fresh'])
        for i in range(nof_ranges):
            if i < nof_ranges-1:
                if self.puzzle['fresh'][i][1] >= self.puzzle['fresh'][i+1][0]:
                    self.puzzle['fresh'][i][1] = self.puzzle['fresh'][i+1][0] - 1
            fresh_total += (self.puzzle['fresh'][i][1] - self.puzzle['fresh'][i][0] + 1)
        return fresh_total


def main() -> dict[str, str]:  # pragma: no cover
    today = y25d05()
    today.solve()
    return today.answer


if __name__ == "__main__":  # pragma: no cover
    answer = main()
    print(f'Part 1: {answer['part_1']}')
    print(f'Part 2: {answer['part_2']}')
