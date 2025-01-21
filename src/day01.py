import sys

import inputfetcher

EXAMPLE = """\
3   4
4   3
2   5
1   3
3   9
3   3\
"""


def parse_input(use_example=False):
    data = EXAMPLE if use_example else inputfetcher.fetch_input('2024', '1')
    list_a = []
    list_b = []
    for line in data.split('\n'):
        a, b = line.split()
        list_a.append(int(a))
        list_b.append(int(b))
    return list_a, list_b


def solve_1(list_a, list_b):
    list_a.sort()
    list_b.sort()
    return sum([abs(a-b) for a, b in zip(list_a, list_b)])


def solve_2(list_a, list_b):
    return sum([list_b.count(id) * id for id in list_a])


if __name__ == "__main__":
    use_example = "--example" in sys.argv
    list_a, list_b = parse_input(use_example)
    result_1 = solve_1(list_a, list_b)
    if use_example:
        assert result_1 == 11, result_1
    print(f'Result 1: {result_1}')
    result_2 = solve_2(list_a, list_b)
    if use_example:
        assert result_2 == 31, result_2
    print(f'Result 2: {result_2}')
