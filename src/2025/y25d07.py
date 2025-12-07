from Day import Day
from Map import Map


class y25d07(Day):

    def __init__(self,
                 auto_fetch: bool = True,
                 auto_parse: bool = True) -> None:
        super().__init__(year='2025', day='07', auto_fetch=auto_fetch, auto_parse=auto_parse)

    def parse_puzzle(self) -> None:
        super().parse_puzzle()
        self.puzzle = Map(self.puzzle_raw, str)

    def solve_part_1(self) -> int:
        beam_split_count = 0
        for c, e in self.puzzle.enumerate_map():
            neighbors = self.puzzle.get_neighbors_by_direction(c, '^')
            if not neighbors['^']:
                continue
            if neighbors['^'][0][1] in ['S', '|']:
                if e == '.':
                    self.puzzle.set_element(c, '|')
                elif e == '^':
                    beam_split_count += 1
                    for d in '<>':
                        if self.puzzle.get_element(c + self.puzzle.COMPASS[d]) != '^':
                            self.puzzle.set_element(c + self.puzzle.COMPASS[d], '|')
        return beam_split_count

    def solve_part_2(self) -> int:
        return 0


def main() -> dict[str, str]:  # pragma: no cover
    today = y25d07()
    today.solve()
    return today.answer


if __name__ == "__main__":  # pragma: no cover
    answer = main()
    print(f'Part 1: {answer['part_1']}')
    print(f'Part 2: {answer['part_2']}')
