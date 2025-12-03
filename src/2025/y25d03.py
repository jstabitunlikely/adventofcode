import re
from Day import Day


class y25d03(Day):

    def __init__(self,
                 auto_fetch: bool = True,
                 auto_parse: bool = True) -> None:
        super().__init__(year='2025', day='03', auto_fetch=auto_fetch, auto_parse=auto_parse)

    def parse_puzzle(self) -> None:
        super().parse_puzzle()
        banks: list[list[int]] = []
        for bank in self.puzzle_raw.strip().split('\n'):
            batteries = [int(b) for b in list(bank)]
            banks.append(batteries)
        self.puzzle = banks

    def solve_part_1(self) -> int:
        joltage = 0
        for i, bank in enumerate(self.puzzle):
            max_index = max(range(len(bank)), key=bank.__getitem__)
            if max_index == len(bank) - 1:
                jolts = 10 * + max(bank[:max_index]) + bank[max_index]
            else:
                jolts = 10 * bank[max_index] + max(bank[max_index+1:])
            joltage += jolts
        return joltage

    def solve_part_2(self) -> int:
        answer = 0
        return answer


def main() -> dict[str, str]:  # pragma: no cover
    today = y25d03()
    today.solve()
    return today.answer


if __name__ == "__main__":  # pragma: no cover
    answer = main()
    print(f'Part 1: {answer['part_1']}')
    print(f'Part 2: {answer['part_2']}')
