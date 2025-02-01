import pytest
from Day01 import Day01


EXAMPLE = """\
3   4
4   3
2   5
1   3
3   9
3   3\
"""


EXPECTED = {
    'part_1': 11,
    'part_2': 31,
}


@pytest.fixture
def answer():
    today = Day01(auto_fetch=False)
    today.puzzle_raw = EXAMPLE
    today.parse_puzzle()
    today.solve()
    return today.answer


def test_answer_part_1(answer):
    assert answer['part_1'] == EXPECTED['part_1']


def test_answer_part_2(answer):
    assert answer['part_2'] == EXPECTED['part_2']
