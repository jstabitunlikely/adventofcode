#!/usr/bin/python3

import inputfetcher
import re


def parse_input():
    return inputfetcher.fetch_input('2024', '3')


def mul(a, b):
    return a*b


def solve_1(mem_contents):
    mul_instr_re = re.compile(r'mul\(\d{1,3},\d{1,3}\)')
    muls = re.findall(mul_instr_re, mem_contents)
    return sum([int(eval(m)) for m in muls])


def solve_2(mem_contents):
    disabled_re = re.compile(r'don\'t\(\).*?do\(\)', re.DOTALL)
    return solve_1(re.sub(disabled_re, '', mem_contents))


if __name__ == "__main__":
    mem_contents = parse_input()
    result_1 = solve_1(mem_contents)
    print(f'Result 1: {result_1}')
    result_2 = solve_2(mem_contents)
    print(f'Result 2: {result_2}')
