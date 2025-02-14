import pytest
from Day20 import Day20


EXAMPLE = """\
###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############\
"""

EXPECTED = {
    'part_1': 44,
    'part_2': 285
}


@pytest.fixture
def today():
    today = Day20(auto_fetch=False)
    today.puzzle_raw = EXAMPLE
    today.parse_puzzle()
    return today


def test_answer_part_1(today):
    answer = today.solve_part_1(limit=0)
    assert answer == EXPECTED['part_1']


def test_answer_part_2(today):
    answer = today.solve_part_2(limit=50)
    assert answer == EXPECTED['part_2']
