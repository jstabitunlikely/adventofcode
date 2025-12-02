import re
from Day import Day


class y25d02(Day):

    def __init__(self,
                 auto_fetch: bool = True,
                 auto_parse: bool = True) -> None:
        super().__init__(year='2025', day='02', auto_fetch=auto_fetch, auto_parse=auto_parse)
        self.INVALID_ID_RE_1 = re.compile(r'^([0-9]+)\1$')
        self.INVALID_ID_RE_2 = re.compile(r'^([0-9]+)\1+$')

    def parse_puzzle(self) -> None:
        super().parse_puzzle()
        ranges = []
        for r in self.puzzle_raw.split(','):
            min, max = r.split('-')
            ranges.append((int(min), int(max)))
        self.puzzle = ranges

    # TODO Merge solution 1-2 on a rainy day

    def solve_part_1(self) -> int:
        answer = 0
        for r in self.puzzle:
            for i in range(r[0], r[1]+1):
                i_str = str(i)
                if self.INVALID_ID_RE_1.search(i_str):
                    answer += i
        return answer

    def solve_part_2(self) -> int:
        answer = 0
        for r in self.puzzle:
            for i in range(r[0], r[1]+1):
                i_str = str(i)
                if self.INVALID_ID_RE_2.search(i_str):
                    answer += i
        return answer


def main() -> dict[str, str]:  # pragma: no cover
    today = y25d02()
    today.solve()
    return today.answer


if __name__ == "__main__":  # pragma: no cover
    answer = main()
    print(f'Part 1: {answer['part_1']}')
    print(f'Part 2: {answer['part_2']}')
