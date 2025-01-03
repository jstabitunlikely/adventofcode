import sys
import math

import inputfetcher


EXAMPLE = """125 17"""


def parse_input(example: bool) -> list[list[str]]:
    data = EXAMPLE if example else inputfetcher.fetch_input('2024', '11')
    return [int(n) for n in data.split()]


def blink(stone: int,
          blinks: int,
          memo: dict) -> list[int]:
    if (stone, blinks) in memo:
        return memo[(stone, blinks)]
    if not blinks:
        return 0
    # Rule #1
    if stone == 0:
        new_stones = blink(1, blinks-1, memo)
    # Rule #2
    # Note: Zero and negative numbers are not handled
    elif not (dc := int(math.log10(stone)) + 1) % 2:
        new_stones = 1
        top = int(stone / (10**(dc/2)))
        bottom = int(stone % (10**(dc/2)))
        new_stones += blink(top, blinks-1, memo)
        new_stones += blink(bottom, blinks-1, memo)
    # Rules #3
    else:
        new_stones = blink(stone*2024, blinks-1, memo)
    memo[(stone, blinks)] = new_stones
    return new_stones


def solve_1_2(stones: list[int],
              blinks: int = 1) -> int:
    new_stones = [blink(s, blinks, {}) for s in stones]
    return len(stones) + sum(new_stones)


if __name__ == "__main__":
    use_example = "--example" in sys.argv
    stones = parse_input(use_example)
    result_1 = solve_1_2(stones, blinks=25)
    print(f'Result 1: {result_1}')
    result_2 = solve_1_2(stones, blinks=75)
    print(f'Result 2: {result_2}')
