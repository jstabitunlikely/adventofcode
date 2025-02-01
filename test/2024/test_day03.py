import pytest
from Day03 import Day03


EXAMPLE_PART_1 = """\
xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))\
"""

EXAMPLE_PART_2 = """\
xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))\
"""


EXPECTED = {
    'part_1': 161,
    'part_2': 48,
}


@pytest.fixture
def today():
    today = Day03(auto_fetch=False)
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
