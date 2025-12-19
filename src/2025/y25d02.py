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

    def get_num_of_invalid_ids(self, pattern):
        num_of_ids = 0
        for r in self.puzzle:
            for i in range(r[0], r[1]+1):
                i_str = str(i)
                if pattern.search(i_str):
                    num_of_ids += i
        return num_of_ids

    def solve_part_1(self) -> int:
        return self.get_num_of_invalid_ids(self.INVALID_ID_RE_1)

    def solve_part_2(self) -> int:
        return self.get_num_of_invalid_ids(self.INVALID_ID_RE_2)


def main() -> dict[str, int]:  # pragma: no cover
    today = y25d02()
    today.solve()
    return today.answer


if __name__ == "__main__":  # pragma: no cover
    answer = main()
    print(f'Part 1: {answer['part_1']}')
    print(f'Part 2: {answer['part_2']}')
