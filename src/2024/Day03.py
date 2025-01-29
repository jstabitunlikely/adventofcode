import re

from Day import Day


class Day03(Day):

    def __init__(self,
                 auto_fetch: bool = True,
                 auto_parse: bool = True) -> None:
        super().__init__(year='2024', day='03', auto_fetch=auto_fetch, auto_parse=auto_parse)

    def parse_puzzle(self) -> None:
        super().parse_puzzle()
        self.puzzle = self.puzzle_raw

    def solve_part_1(self, **kwargs) -> int:
        puzzle = kwargs.get('puzzle', self.puzzle)
        mul_instr_re = re.compile(r'mul\(\d{1,3},\d{1,3}\)')
        muls = re.findall(mul_instr_re, puzzle)
        muldef = {'mul': lambda a, b: a*b}
        answer = sum([int(eval(m, muldef)) for m in muls])
        return answer

    def solve_part_2(self) -> int:
        disabled_re = re.compile(r'don\'t\(\).*?do\(\)', re.DOTALL)
        p = re.sub(disabled_re, '', self.puzzle)
        answer = self.solve_part_1(puzzle=p)
        return answer


def main() -> dict[str, str]:  # pragma: no cover
    today = Day03()
    today.solve()
    return today.answer


if __name__ == "__main__":  # pragma: no cover
    answer = main()
    print(f'Part 1: {answer['part_1']}')
    print(f'Part 2: {answer['part_2']}')
