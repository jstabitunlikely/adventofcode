import inputfetcher
import sys

EXAMPLE = """\
190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20\
"""


def parse_input(use_example: bool) -> list[tuple[int, list[int]]]:
    data = EXAMPLE if use_example else inputfetcher.fetch_input('2024', '7')
    equations = data.split('\n')
    equations = [e.split(':') for e in equations]
    equations = [[e[0], e[1].split()] for e in equations]
    equations = [(int(e[0]), [int(n) for n in e[1]]) for e in equations]
    return equations


def maths(tv: int,
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
        a = maths(tv, ptv_a, n[1:], cen)
    if ptv_m <= tv:
        m = maths(tv, ptv_m, n[1:], cen)
    if cen and ptv_c <= tv:
        c = maths(tv, ptv_c, n[1:], cen)
    return a or m or c


def solve_1_2(equations: list[tuple[int, list[int]]],
              cen: bool = False) -> int:
    cv = 0
    for tv, n in equations:
        if maths(tv, n[0], n[1:], cen):
            cv += tv
    return cv


if __name__ == "__main__":
    use_example = "--example" in sys.argv
    equations = parse_input(use_example)
    result_1 = solve_1_2(equations, cen=False)
    if use_example:
        assert result_1 == 3749, result_1
    print(f'Result 1: {result_1}')
    result_2 = solve_1_2(equations, cen=True)
    if use_example:
        assert result_2 == 11387, result_2
    print(f'Result 2: {result_2}')
