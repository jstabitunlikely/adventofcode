import sys
from itertools import permutations

import inputfetcher
import RadixTrie

EXAMPLE = """\
r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb\
"""


def parse_input(example: bool) -> tuple[list[str], list[str]]:
    data = EXAMPLE if example else inputfetcher.fetch_input('2024', '19')
    data = data.strip()
    words, designs = data.split('\n\n')
    words = words.split(',')
    words = [w.strip() for w in words]
    designs = designs.split('\n')
    return words, designs


def solve_1(words: list[str],
            designs: list[str]) -> int:
    rt = RadixTrie.RadixTrie()
    rt.add_many(words)

    # Test 1: each words must be found
    is_word = [rt.is_word(w) for w in words]
    assert all(is_word)
    # Test 2: generate n-word sentences and find them
    n = 2
    for w in permutations(words, n):
        test_sentence = ''.join(w)
        is_sentence = rt.is_sentence(test_sentence), f'{test_sentence}'
        assert is_sentence, f'{test_sentence}'

    return len([d for d in designs if rt.is_sentence(d)])


def solve_2(words: list[str],
            designs: list[str]) -> int:
    return None


if __name__ == "__main__":
    use_example = "--example" in sys.argv
    words, designs = parse_input(use_example)
    result_1 = solve_1(words, designs)
    if use_example:
        assert result_1 == 6, result_1
    print(f'Result 1: {result_1}')
    result_2 = solve_2(words, designs)
    print(f'Result 2: {result_2}')
