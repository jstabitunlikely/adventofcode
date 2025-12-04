from Day import Day
from Map import Map


class y25d04(Day):

    def __init__(self,
                 auto_fetch: bool = True,
                 auto_parse: bool = True) -> None:
        super().__init__(year='2025', day='04', auto_fetch=auto_fetch, auto_parse=auto_parse)

    def parse_puzzle(self) -> None:
        super().parse_puzzle()
        self.puzzle = Map(self.puzzle_raw, str)

    def solve_part_1(self) -> int:
        free_rolls = 0
        for coordinate in self.puzzle.find_all_element('@'):
            neighbors = self.puzzle.get_neighbors_around(coordinate, 1, )
            free_rolls += 1 if (neighbors.count('@') < 4) else 0
        return free_rolls

    def solve_part_2(self) -> int:
        return 0


def main() -> dict[str, str]:  # pragma: no cover
    today = y25d04()
    today.solve()
    return today.answer


if __name__ == "__main__":  # pragma: no cover
    answer = main()
    print(f'Part 1: {answer['part_1']}')
    print(f'Part 2: {answer['part_2']}')
