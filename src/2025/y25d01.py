from Day import Day


class y25d01(Day):

    def __init__(self,
                 auto_fetch: bool = True,
                 auto_parse: bool = True) -> None:
        super().__init__(year='2025', day='01', auto_fetch=auto_fetch, auto_parse=auto_parse)
        self.DIAL_SIZE = 100
        self.STARTING_POSITION = 50

    def parse_puzzle(self) -> None:
        super().parse_puzzle()
        turns = []
        for line in self.puzzle_raw.split('\n'):
            turns.append(int(line[1:]))
            if line.startswith('L'):
                turns[-1] = -1 * turns[-1]
        self.puzzle = turns

    def solve_part_1(self) -> int:
        answer = 0
        current_position = self.STARTING_POSITION
        for t in self.puzzle:
            current_position += t
            answer += not (current_position % self.DIAL_SIZE)
        return answer

    def solve_part_2(self) -> int:
        zero_crossings = 0
        current_position = self.STARTING_POSITION
        for t in self.puzzle:
            if t >= 0:
                current_position += t
                zero_crossings += (current_position // self.DIAL_SIZE)
                current_position %= self.DIAL_SIZE
            else:
                # Solve this in the Upside down
                current_position = ((self.DIAL_SIZE-current_position) % self.DIAL_SIZE)
                current_position -= t
                zero_crossings += (current_position // self.DIAL_SIZE)
                current_position %= self.DIAL_SIZE
                # We have to go back
                current_position = ((self.DIAL_SIZE-current_position) % self.DIAL_SIZE)
        return zero_crossings


def main() -> dict[str, str]:  # pragma: no cover
    today = y25d01()
    today.solve()
    return today.answer


if __name__ == "__main__":  # pragma: no cover
    answer = main()
    print(f'Part 1: {answer['part_1']}')
    print(f'Part 2: {answer['part_2']}')
