import pytest
from y25d09 import y25d09


EXAMPLE = """\
7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3\
"""


EXPECTED = {
    'part_1': 50,
    'part_2': 0,
}


@pytest.fixture
def answer():
    today = y25d09(auto_fetch=False)
    today.puzzle_raw = EXAMPLE
    today.parse_puzzle()
    today.solve()
    return today.answer


def test_answer_part_1(answer):
    assert answer['part_1'] == EXPECTED['part_1']


def test_answer_part_2(answer):
    assert answer['part_2'] == EXPECTED['part_2']
