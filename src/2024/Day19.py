from Day import Day
import RadixTrie


class Day19(Day):

    def __init__(self,
                 auto_fetch: bool = True,
                 auto_parse: bool = True) -> None:
        super().__init__(year='2024', day='19', auto_fetch=auto_fetch, auto_parse=auto_parse)

    def parse_puzzle(self) -> None:
        self.puzzle_raw = self.puzzle_raw.strip()
        words, designs = self.puzzle_raw.split('\n\n')
        words_split = words.split(',')
        words_split = [w.strip() for w in words_split]
        designs_split = designs.split('\n')
        self.puzzle = {
            'words': words_split,
            'designs': designs_split,
        }

    def solve_part_1(self):
        rt = RadixTrie.RadixTrie()
        rt.add_many(self.puzzle['words'])
        valid_sentences = [d for d in self.puzzle['designs'] if rt.is_sentence(d)]
        possible_sentences = [rt.possible_sentences(s) for s in valid_sentences]
        return {
            'part_1': len(valid_sentences),
            'part_2': sum(possible_sentences),
        }

    solve_part_2 = solve_part_1


def main() -> dict[str, int]:  # pragma: no cover
    today = Day19()
    today.solve()
    return today.answer


if __name__ == "__main__":  # pragma: no cover
    answer = main()
    print(f'Part 1: {answer['part_1']}')
    print(f'Part 2: {answer['part_2']}')
