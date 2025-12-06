from Day import Day
from utils import transpose
from typing import Any


class y25d06(Day):

    def __init__(self,
                 auto_fetch: bool = True,
                 auto_parse: bool = True) -> None:
        super().__init__(year='2025', day='06', auto_fetch=auto_fetch, auto_parse=auto_parse)

    def parse_puzzle(self) -> None:
        super().parse_puzzle()
        rows = self.puzzle_raw.split('\n')
        self.puzzle: dict[str, list[Any]] = {
            'inputs': rows[:-1],
            'operators': rows[-1].split()
        }

    def solve_part_1(self) -> int:
        result = 0
        inputs = []
        for row in self.puzzle['inputs']:
            inputs.append(row.split())
        inputs_t = transpose(inputs)
        for i, operands in enumerate(inputs_t):
            result += eval(self.puzzle['operators'][i].join(operands))
        return result

    def solve_part_2(self) -> int:
        return 0


def main() -> dict[str, str]:  # pragma: no cover
    today = y25d06()
    today.solve()
    return today.answer


if __name__ == "__main__":  # pragma: no cover
    answer = main()
    print(f'Part 1: {answer['part_1']}')
    print(f'Part 2: {answer['part_2']}')
