from Day import Day
from utils import sign


class Day02(Day):

    def __init__(self,
                 auto_fetch: bool = True,
                 auto_parse: bool = True) -> None:
        super().__init__(year='2024', day='02', auto_fetch=auto_fetch, auto_parse=auto_parse)

    def parse_puzzle(self):
        super().parse_puzzle()
        reports = []
        for line in self.puzzle_raw.split('\n'):
            reports.append([int(x) for x in line.split()])
        self.puzzle = reports

    def solve_part_1(self, **kwargs) -> int:
        puzzle = kwargs.get('puzzle', self.puzzle)
        safe = 0
        for report in puzzle:
            report_d = [y-x for x, y in zip(report, report[1:])]
            if [d for d in report_d if abs(d) > 3]:
                continue
            if len(set([sign(d) for d in report_d])) > 1:
                continue
            safe += 1
        return safe

    def solve_part_2(self) -> int:
        safe = 0
        for report in self.puzzle:
            if self.solve_part_1(puzzle=[report]):
                safe += 1
                continue
            for i in range(len(report)):
                p = [report[:i]+report[i+1:]]
                if self.solve_part_1(puzzle=p):
                    safe += 1
                    break
        return safe


def main() -> dict[str, int]:  # pragma: no cover
    today = Day02()
    today.solve()
    return today.answer


if __name__ == "__main__":  # pragma: no cover
    answer = main()
    print(f'Part 1: {answer['part_1']}')
    print(f'Part 2: {answer['part_2']}')
