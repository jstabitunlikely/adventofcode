import sys

import inputfetcher
from utils import sign

EXAMPLE = """\
7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9\
"""


def parse_input(use_example=False):
    data = EXAMPLE if use_example else inputfetcher.fetch_input('2024', '2')
    reports = []
    for line in data.split('\n'):
        reports.append([int(x) for x in line.split()])
    return reports


def solve_1(reports):
    safe = 0
    for report in reports:
        report_d = [y-x for x, y in zip(report, report[1:])]
        if [d for d in report_d if abs(d) > 3]:
            continue
        if len(set([sign(d) for d in report_d])) > 1:
            continue
        safe += 1
    return safe


def solve_2(reports):
    safe = 0
    for report in reports:
        if solve_1([report]):
            safe += 1
            continue
        for i in range(len(report)):
            if solve_1([report[:i]+report[i+1:]]):
                safe += 1
                break
    return safe


if __name__ == "__main__":
    use_example = "--example" in sys.argv
    reports = parse_input(use_example)
    result_1 = solve_1(reports)
    if use_example:
        assert result_1 == 2, result_1
    print(f'Result 1: {result_1}')
    result_2 = solve_2(reports)
    if use_example:
        assert result_2 == 4, result_2
    print(f'Result 2: {result_2}')
