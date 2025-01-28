import re
import sys

import inputfetcher


EXAMPLE_1 = """\
xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))\
"""

EXAMPLE_2 = """\
xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))\
"""


def parse_input(use_example=0):
    match use_example:
        case 0:
            return inputfetcher.fetch_input('2024', '3')
        case 1:
            return EXAMPLE_1
        case 2:
            return EXAMPLE_2


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
    use_example = "--example" in sys.argv
    mem_contents = parse_input(use_example=0)
    # Part 1
    if use_example:
        mem_contents = parse_input(use_example=1)
    result_1 = solve_1(mem_contents)
    if use_example:
        assert result_1 == 161, result_1
    print(f'Result 1: {result_1}')
    # Part 2
    if use_example:
        mem_contents = parse_input(use_example=2)
    result_2 = solve_2(mem_contents)
    if use_example:
        assert result_2 == 48, result_2
    print(f'Result 2: {result_2}')
