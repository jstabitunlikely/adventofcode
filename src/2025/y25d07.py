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

    def solve_part_1(self) -> dict[str, int]:
        ABOVE = self.puzzle.COMPASS['^']
        LEFT = self.puzzle.COMPASS['<']
        RIGHT = self.puzzle.COMPASS['>']

        start = self.puzzle.find_first_element('S')
        self.puzzle.set_element(start, 1)

        for c in self.puzzle.find_all_element('.'):
            self.puzzle.set_element(c, 0)

        beam_split_count = 0
        for c, e in self.puzzle.enumerate_map():
            if c.x == 0:
                continue
            current_timelines = 0

            above = self.puzzle.get_element(c + ABOVE, False)
            if isinstance(above, int):
                if e == '^' and above > 0:
                    beam_split_count += 1
                    continue
                else:
                    current_timelines += above

            left = self.puzzle.get_element(c + LEFT, False)
            if left is not None and left == '^':
                if isinstance(self.puzzle.get_element(c + LEFT + ABOVE), int):
                    current_timelines += self.puzzle.get_element(c + LEFT + ABOVE)

            right = self.puzzle.get_element(c + RIGHT, False)
            if right is not None and right == '^':
                if isinstance(self.puzzle.get_element(c + RIGHT + ABOVE), int):
                    current_timelines += self.puzzle.get_element(c + RIGHT + ABOVE)

            self.puzzle.set_element(c, current_timelines)

        timelines = sum([o for o in self.puzzle.map_[-1] if isinstance(o, int)])
        return {
            'part_1': beam_split_count,
            'part_2': timelines,
        }

    solve_part_2 = solve_part_1


def main() -> dict[str, int]:  # pragma: no cover
    today = y25d07()
    today.solve()
    return today.answer


if __name__ == "__main__":  # pragma: no cover
    answer = main()
    print(f'Part 1: {answer['part_1']}')
    print(f'Part 2: {answer['part_2']}')
