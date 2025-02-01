import pytest
from Day16 import Day16

EXAMPLE_1 = """\
###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############\
"""

EXPECTED_1 = {
    'part_1': 7036,
    'part_2': 45,
}


EXAMPLE_2 = """\
#################
#...#...#...#..E#
#.#.#.#.#.#.#.#.#
#.#.#.#...#...#.#
#.#.#.#.###.#.#.#
#...#.#.#.....#.#
#.#.#.#.#.#####.#
#.#...#.#.#.....#
#.#.#####.#.###.#
#.#.#.......#...#
#.#.###.#####.###
#.#.#...#.....#.#
#.#.#.#####.###.#
#.#.#.........#.#
#.#.#.#########.#
#S#.............#
#################\
"""

EXPECTED_2 = {
    'part_1': 11048,
    'part_2': 64,
}


@pytest.fixture
def answer_1():
    today = Day16(auto_fetch=False)
    today.puzzle_raw = EXAMPLE_1
    today.parse_puzzle()
    today.solve()
    return today.answer


def test_answer_1_part_1(answer_1):
    assert answer_1['part_1'] == EXPECTED_1['part_1']


def test_answer_1_part_2(answer_1):
    assert answer_1['part_2'] == EXPECTED_1['part_2']


@pytest.fixture
def answer_2():
    today = Day16(auto_fetch=False)
    today.puzzle_raw = EXAMPLE_2
    today.parse_puzzle()
    today.solve()
    return today.answer


def test_answer_2_part_1(answer_2):
    assert answer_2['part_1'] == EXPECTED_2['part_1']


def test_answer_2_part_2(answer_2):
    assert answer_2['part_2'] == EXPECTED_2['part_2']
