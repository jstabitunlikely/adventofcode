from Day import Day


class Day07(Day):

    def __init__(self,
                 auto_fetch: bool = True,
                 auto_parse: bool = True) -> None:
        super().__init__(year='2024', day='07', auto_fetch=auto_fetch, auto_parse=auto_parse)

    def parse_puzzle(self) -> None:
        equations1 = self.puzzle_raw.split('\n')
        equations2 = [e.split(':') for e in equations1]
        equations3 = [[e[0], e[1].split()] for e in equations2]
        equations4 = [(int(e[0]), [int(n) for n in e[1]]) for e in equations3]  # type:ignore
        self.puzzle = equations4

    def maths(self,
              tv: int,
              ptv: int,
              n: list[int],
              cen: bool = False) -> bool:
        if not n:
            return ptv == tv
        ptv_a = ptv + n[0]
        ptv_m = ptv * n[0]
        if cen:
            ptv_c = int(str(ptv) + str(n[0]))
        a = m = c = False
        if ptv_a <= tv:
            a = self.maths(tv, ptv_a, n[1:], cen)
        if ptv_m <= tv:
            m = self.maths(tv, ptv_m, n[1:], cen)
        if cen and ptv_c <= tv:
            c = self.maths(tv, ptv_c, n[1:], cen)
        return a or m or c

    def solve_part_1(self, cen: bool = False) -> int:
        cv = 0
        for tv, n in self.puzzle:
            if self.maths(tv, n[0], n[1:], cen):
                cv += tv
        return cv

    def solve_part_2(self) -> int:
        return self.solve_part_1(cen=True)


def main() -> dict[str, str]:  # pragma: no cover
    today = Day07()
    today.solve()
    return today.answer


if __name__ == "__main__":  # pragma: no cover
    answer = main()
    print(f'Part 1: {answer['part_1']}')
    print(f'Part 2: {answer['part_2']}')
