import math
from Day import Day


class Day11(Day):

    def __init__(self,
                 auto_fetch: bool = True,
                 auto_parse: bool = True) -> None:
        super().__init__(year='2024', day='11', auto_fetch=auto_fetch, auto_parse=auto_parse)

    def parse_puzzle(self) -> None:
        self.puzzle = [int(n) for n in self.puzzle_raw.split()]

    def evolve(self,
               stone: int) -> list[int]:
        if not stone:
            return [1]
        if not (dc := math.floor(math.log10(stone)) + 1) % 2:
            return [stone % (10**(dc//2)), stone // (10**(dc//2))]
        return [stone * 2024]

    def blink(self,
              stone: int,
              blinks: int,
              memo: dict) -> int:
        if not blinks:
            return 0
        if (m := memo.get((stone, blinks), None)) is not None:
            return m
        evolved_stones = self.evolve(stone)
        num_stones = len(evolved_stones) - 1
        num_stones += sum([self.blink(s, blinks-1, memo) for s in evolved_stones])
        memo[(stone, blinks)] = num_stones
        return num_stones

    def solve_part_1(self, blinks: int = 25) -> int:
        memo: dict[tuple[int, int], int] = {}
        return len(self.puzzle) + sum([self.blink(s, blinks, memo) for s in self.puzzle])

    def solve_part_2(self, blinks: int = 75) -> int:
        return self.solve_part_1(blinks=blinks)


def main() -> dict[str, str]:  # pragma: no cover
    today = Day11()
    today.solve()
    return today.answer


if __name__ == "__main__":  # pragma: no cover
    answer = main()
    print(f'Part 1: {answer['part_1']}')
    print(f'Part 2: {answer['part_2']}')
