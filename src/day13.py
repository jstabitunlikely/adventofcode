import re
import sys

import math
import numpy as np
from scipy import linalg

import inputfetcher

EXAMPLE = """\
Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279\
"""


def parse_input(example):
    data = EXAMPLE if example else inputfetcher.fetch_input('2024', '13')
    data = data.split('\n\n')
    numbers_re = re.compile(r'\d+', flags=re.DOTALL)
    machines = []
    for ax, ay, bx, by, px, py in [re.findall(numbers_re, m) for m in data]:
        a = np.array([[ax, bx], [ay, by]], dtype=int)
        b = np.array([px, py], dtype=int)
        machines.append([a, b])
    return machines


def is_int(number):
    return math.isclose(number, round(number))


def solve_1(machines):
    cost = [3, 1]
    tokens = 0
    for a, b in machines:
        x = linalg.solve(a, b, check_finite=False)
        # No solution at all
        if not len(x):
            continue
        # No solution over integers
        if not all([is_int(n) for n in x]):
            continue
        tokens += np.dot(cost, x)
    return int(tokens)


if __name__ == "__main__":
    use_example = "--example" in sys.argv
    machines = parse_input(use_example)
    result_1 = solve_1(machines)
    print(f'Result 1: {result_1}')
