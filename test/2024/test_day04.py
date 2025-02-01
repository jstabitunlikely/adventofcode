import pytest
from Day04 import Day04


EXAMPLE_PART_1 = """\
MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX\
"""

EXAMPLE_PART_2 = """\
.M.S......
..A..MSMS.
.M.S.MAA..
..A.ASMSM.
.M.S.M....
..........
S.S.S.S.S.
.A.A.A.A..
M.M.M.M.M.
..........\
"""


EXPECTED = {
    'part_1': 18,
    'part_2': 9,
}


@pytest.fixture
def today():
    today = Day04(auto_fetch=False)
    return today


def test_answer_part_1(today):
    today.puzzle_raw = EXAMPLE_PART_1
    today.parse_puzzle()
    answer = today.solve_part_1()
    assert answer == EXPECTED['part_1']


def test_answer_part_2(today):
    today.puzzle_raw = EXAMPLE_PART_2
    today.parse_puzzle()
    answer = today.solve_part_2()
    assert answer == EXPECTED['part_2']
