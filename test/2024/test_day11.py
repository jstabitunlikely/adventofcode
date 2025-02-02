import pytest
from Day11 import Day11


EXAMPLE = """\
125 17\
"""

EXPECTED = {
    'part_1': 55312,
    'part_2': 65601038650482,
}


@pytest.fixture
def answer():
    today = Day11(auto_fetch=False)
    today.puzzle_raw = EXAMPLE
    today.parse_puzzle()
    today.solve()
    return today.answer


def test_answer_part_1(answer):
    assert answer['part_1'] == EXPECTED['part_1']


def test_answer_part_2(answer):
    assert answer['part_2'] == EXPECTED['part_2']
