import pytest
from Day25 import Day25


EXAMPLE = """\
#####
.####
.####
.####
.#.#.
.#...
.....

#####
##.##
.#.##
...##
...#.
...#.
.....

.....
#....
#....
#...#
#.#.#
#.###
#####

.....
.....
#.#..
###..
###.#
###.#
#####

.....
.....
.....
#....
#.#..
#.#.#
#####\
"""

EXPECTED = {
    'part_1': 3,
}


@pytest.fixture
def today():
    today = Day25(auto_fetch=False)
    today.puzzle_raw = EXAMPLE
    today.parse_puzzle()
    return today


def test_answer_part_1(today):
    answer = today.solve_part_1()
    assert answer == EXPECTED['part_1']
