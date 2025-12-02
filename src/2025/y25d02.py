from Day import Day


class y25d02(Day):

    def __init__(self,
                 auto_fetch: bool = True,
                 auto_parse: bool = True) -> None:
        super().__init__(year='2025', day='02', auto_fetch=auto_fetch, auto_parse=auto_parse)

    def parse_puzzle(self) -> None:
        super().parse_puzzle()
        ranges = []
        for r in self.puzzle_raw.split(','):
            min, max = r.split('-')
            ranges.append((int(min), int(max)))
        self.puzzle = ranges

    def solve_part_1(self) -> int:
        answer = 0
        for r in self.puzzle:
            for i in range(r[0], r[1]+1):
                idx = len(str(i)) // 2
                i_str = str(i)
                if (i_str[:idx] == i_str[idx:]):
                    answer += i
        return answer

    def solve_part_2(self) -> int:
        return 0


def main() -> dict[str, str]:  # pragma: no cover
    today = y25d02()
    today.solve()
    return today.answer


if __name__ == "__main__":  # pragma: no cover
    answer = main()
    print(f'Part 1: {answer['part_1']}')
    print(f'Part 2: {answer['part_2']}')
