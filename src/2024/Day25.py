from Day import Day
import numpy as np
import numpy.typing as npt
from itertools import product

from Map import Map


class Day25(Day):

    def __init__(self,
                 auto_fetch: bool = True,
                 auto_parse: bool = True) -> None:
        super().__init__(year='2024', day='25', auto_fetch=auto_fetch, auto_parse=auto_parse)

    def parse_puzzle(self) -> None:
        schematics = self.puzzle_raw.split('\n\n')
        schematics_digital: dict[str, list[npt.NDArray]] = {
            'locks': [],
            'keys': [],
        }
        for sch in schematics:
            sch_str = Map(sch, str)
            sch_int = [list(map(lambda x: 1 if x == '#' else 0, line)) for line in sch_str.map_]
            sch_arr = np.array(sch_int)
            if all(sch_arr[0]):
                k = 'keys'
            elif all(sch_arr[-1]):
                k = 'locks'
            schematics_digital[k].append(sch_arr)
        self.puzzle = schematics_digital

    def solve_part_1(self) -> int:
        fits = 0
        for lock, key in product(self.puzzle['keys'], self.puzzle['locks']):
            fits += not np.any(np.bitwise_and(lock, key))
        return fits

    def solve_part_2(self) -> str:
        return 'Merry Christmas!'


def main() -> dict[str, int]:  # pragma: no cover
    today = Day25()
    today.solve()
    return today.answer


if __name__ == "__main__":  # pragma: no cover
    answer = main()
    print(f'Part 1: {answer['part_1']}')
    print(f'Part 2: {answer['part_2']}')
