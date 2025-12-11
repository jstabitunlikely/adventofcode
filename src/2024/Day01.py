from Day import Day


class Day01(Day):

    def __init__(self,
                 auto_fetch: bool = True,
                 auto_parse: bool = True) -> None:
        super().__init__(year='2024', day='01', auto_fetch=auto_fetch, auto_parse=auto_parse)

    def parse_puzzle(self) -> None:
        super().parse_puzzle()
        parsed: dict[str, list[int]] = {
            'a': [],
            'b': [],
        }
        for line in self.puzzle_raw.split('\n'):
            a, b = line.split()
            parsed['a'].append(int(a))
            parsed['b'].append(int(b))
        self.puzzle = parsed

    def solve_part_1(self) -> int:
        self.puzzle['a'].sort()
        self.puzzle['b'].sort()
        answer = sum([abs(a-b) for a, b in zip(self.puzzle['a'], self.puzzle['b'])])
        return answer

    def solve_part_2(self) -> int:
        answer = sum([self.puzzle['b'].count(id) * id for id in self.puzzle['a']])
        return answer


def main() -> dict[str, int]:  # pragma: no cover
    today = Day01()
    today.solve()
    return today.answer


if __name__ == "__main__":  # pragma: no cover
    answer = main()
    print(f'Part 1: {answer['part_1']}')
    print(f'Part 2: {answer['part_2']}')
