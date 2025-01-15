import sys

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


def solve_1_2(words: list[str],
              designs: list[str]) -> tuple[int, int]:
    rt = RadixTrie.RadixTrie()
    rt.add_many(words)
    valid_sentences = [d for d in designs if rt.is_sentence(d)]
    possible_sentences = [rt.possible_sentences(s) for s in valid_sentences]
    return len(valid_sentences), sum(possible_sentences)


if __name__ == "__main__":
    use_example = "--example" in sys.argv
    words, designs = parse_input(use_example)
    result_1, result_2 = solve_1_2(words, designs)
    if use_example:
        assert result_1 == 6, result_1
        assert result_2 == 16, result_2
    print(f'Result 1: {result_1}')
    print(f'Result 2: {result_2}')
