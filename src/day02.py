#!/usr/bin/python3

import inputfetcher

def sign(num):
    if num < 0:
        return -1
    if num > 0:
        return 1
    return 0

def parse_input():
    input_text = inputfetcher.fetch_input('2024', '2')
    reports = []
    for line in input_text.split('\n'):
        reports.append([ int(x) for x in line.split()])
    return reports

def solve_1(reports):
    safe = 0
    for report in reports:
        report_d = [y-x for x,y in zip(report, report[1:])]
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
    reports = parse_input()
    result_1 = solve_1(reports)
    print(f'Result 1: {result_1}')
    result_2 = solve_2(reports)
    print(f'Result 2: {result_2}')