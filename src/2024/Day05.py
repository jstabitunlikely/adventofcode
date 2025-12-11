from Day import Day


class Day05(Day):

    def __init__(self,
                 auto_fetch: bool = True,
                 auto_parse: bool = True) -> None:
        super().__init__(year='2024', day='05', auto_fetch=auto_fetch, auto_parse=auto_parse)

    def parse_puzzle(self) -> None:
        # separate the ruleset from the list of page updates
        ruleset, updates = self.puzzle_raw.split('\n\n')
        # convert the ruleset to a list of integer pairs
        ruleset = ruleset.split()  # type:ignore
        ruleset = [list(map(int, r.split('|'))) for r in ruleset]  # type:ignore
        # convert the updates into a lists of integers
        updates = updates.split()  # type:ignore
        updates = [list(map(int, u.split(','))) for u in updates]  # type:ignore
        self.puzzle = {
            'ruleset': ruleset,
            'updates': updates
        }

    def solve_part_1(self) -> dict[str, int]:
        correct = 0
        incorrect = 0
        for update in self.puzzle['updates']:
            update_sorted = sorted(update, key=lambda p:
                                   len([r[0] for r in self.puzzle['ruleset'] if r[1] == p and r[0] in update]))
            middle = update_sorted[int(len(update)/2)]
            if update == update_sorted:
                correct += middle  # type:ignore
            else:
                incorrect += middle  # type:ignore
        return {
            'part_1': correct,
            'part_2': incorrect,
        }

    solve_part_2 = solve_part_1


def main() -> dict[str, int]:  # pragma: no cover
    today = Day05()
    today.solve()
    return today.answer


if __name__ == "__main__":  # pragma: no cover
    answer = main()
    print(f'Part 1: {answer['part_1']}')
    print(f'Part 2: {answer['part_2']}')
