import sys
import math

import InputFetcher


EXAMPLE = """125 17"""


def parse_input(example: bool) -> list[int]:
    data = EXAMPLE if example else InputFetcher.fetch_input('2024', '11')
    return [int(n) for n in data.split()]


def evolve(stone: int) -> list[int]:
    if not stone:
        return [1]
    if not (dc := math.floor(math.log10(stone)) + 1) % 2:
        return [stone % (10**(dc//2)), stone // (10**(dc//2))]
    return [stone * 2024]


def blink(stone: int,
          blinks: int,
          memo: dict) -> int:
    if not blinks:
        return 0
    if (m := memo.get((stone, blinks), None)) is not None:
        return m
    evolved_stones = evolve(stone)
    num_stones = len(evolved_stones) - 1
    num_stones += sum([blink(s, blinks-1, memo) for s in evolved_stones])
    memo[(stone, blinks)] = num_stones
    return num_stones


def solve_1_2(stones: list[int],
              blinks: int = 1) -> int:
    memo: dict[tuple[int, int], int] = {}
    return len(stones) + sum([blink(s, blinks, memo) for s in stones])


if __name__ == "__main__":
    use_example = "--example" in sys.argv
    stones = parse_input(use_example)
    result_1 = solve_1_2(stones, blinks=25)
    if use_example:
        assert result_1 == 55312, result_1
    print(f'Result 1: {result_1}')
    result_2 = solve_1_2(stones, blinks=75)
    if use_example:
        assert result_2 == 65601038650482, result_2
    print(f'Result 2: {result_2}')
