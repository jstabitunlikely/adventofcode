
#!/usr/bin/python3

import inputfetcher
from functools import cmp_to_key
from collections import Counter

EXAMPLE1 = """47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47"""


def parse_input(example1=False, example2=False):
    if example1:
        data = EXAMPLE1
    elif example2:
        data = EXAMPLE2
    else:
        data = inputfetcher.fetch_input('2024', '5')
    # separate the rulesest from the list of page updates
    ruleset, updates = data.split('\n\n')
    # convert the ruleset to a list of integer pairs
    ruleset = ruleset.split()
    ruleset = [list(map(int, r.split('|'))) for r in ruleset]
    # convert the updates into a lists of integers
    updates = updates.split()
    updates = [list(map(int, u.split(','))) for u in updates]
    return [ruleset, updates]


def solve_1_2(ruleset, updates):
    correct = 0
    incorrect = 0
    for update in updates:
        update_sorted = sorted(update, key=lambda p:
                               len([r[0] for r in ruleset if r[1] == p and r[0] in update]))
        middle = update_sorted[int(len(update)/2)]
        if update == update_sorted:
            correct += middle
        else:
            incorrect += middle
    return correct, incorrect


if __name__ == "__main__":
    ruleset, updates = parse_input()
    result_1, result_2 = solve_1_2(ruleset, updates)
    print(f'Result 1: {result_1}')
    print(f'Result 2: {result_2}')
