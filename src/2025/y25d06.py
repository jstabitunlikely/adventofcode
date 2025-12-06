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
        self.puzzle: dict[str, Any] = {
            'inputs': rows[:-1],
            'operators': rows[-1]
        }

    def solve_part_1(self) -> int:
        result = 0
        inputs = [row.split() for row in self.puzzle['inputs']]
        inputs_t = transpose(inputs)
        operators = self.puzzle['operators'].split()
        for i, operands in enumerate(inputs_t):
            result += eval(operators[i].join(operands))
        return result

    def solve_part_2(self) -> int:
        operations_t = transpose(
            [self.puzzle['operators']] +
            self.puzzle['inputs']
        )
        result = 0
        partial_result = ''
        current_operation = ''
        for operation in operations_t:
            current_operand = ''.join(operation[1:]).strip()
            if operation[0] != ' ':
                current_operation = operation[0]
                partial_result = current_operand
                continue
            if current_operand:
                partial_result += current_operation + current_operand
            else:
                result += eval(partial_result)
                partial_result = ''
        result += eval(partial_result)
        return result


def main() -> dict[str, str]:  # pragma: no cover
    today = y25d06()
    today.solve()
    return today.answer


if __name__ == "__main__":  # pragma: no cover
    answer = main()
    print(f'Part 1: {answer['part_1']}')
    print(f'Part 2: {answer['part_2']}')
