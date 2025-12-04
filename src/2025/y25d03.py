from Day import Day


class y25d03(Day):

    def __init__(self,
                 auto_fetch: bool = True,
                 auto_parse: bool = True) -> None:
        super().__init__(year='2025', day='03', auto_fetch=auto_fetch, auto_parse=auto_parse)

    def parse_puzzle(self) -> None:
        super().parse_puzzle()
        banks: list[list[str]] = []
        for bank in self.puzzle_raw.strip().split('\n'):
            banks.append(list(bank))
        self.puzzle = banks

    def get_joltage(self, number_of_batteries=2) -> int:
        joltage = 0
        for bank in self.puzzle:
            first_battery_idx = 0
            for m in range(number_of_batteries, 0, -1):
                last_battery_idx = len(bank)-m+1
                strongest_battery = max(enumerate(bank[first_battery_idx:last_battery_idx]), key=lambda item: item[1])
                first_battery_idx += strongest_battery[0] + 1
                joltage += 10 ** (m-1) * int(strongest_battery[1])
        return joltage

    def solve_part_1(self) -> int:
        return self.get_joltage(2)

    def solve_part_2(self) -> int:
        return self.get_joltage(12)


def main() -> dict[str, str]:  # pragma: no cover
    today = y25d03()
    today.solve()
    return today.answer


if __name__ == "__main__":  # pragma: no cover
    answer = main()
    print(f'Part 1: {answer['part_1']}')
    print(f'Part 2: {answer['part_2']}')
