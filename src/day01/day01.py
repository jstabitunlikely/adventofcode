#!/usr/bin/python3

import inputfetcher

def parse_input():
    input_text = inputfetcher.fetch_input('2024', '1')
    list_a = []
    list_b = []
    for line in input_text.split('\n'):
        a, b = line.split()
        list_a.append(int(a))
        list_b.append(int(b))
    return list_a, list_b

def solve_1(list_a, list_b):
    list_a.sort()
    list_b.sort()
    return sum([abs(a-b) for a,b in zip(list_a, list_b)])
    print(result)

def solve_2(list_a, list_b):
    return sum([list_b.count(id) * id for id in list_a])

if __name__ == "__main__":
    list_a, list_b = parse_input()
    result_1 = solve_1(list_a, list_b)
    print(f'Result 1: {result_1}')
    result_2 = solve_2(list_a, list_b)
    print(f'Result 2: {result_2}')