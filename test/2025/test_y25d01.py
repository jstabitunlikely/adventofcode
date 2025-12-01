import pytest
from y25d01 import y25d01


EXAMPLE = """\
L68
L30
R48
L5
R60
L55
L1
L99
R14
L82\
"""


EXPECTED = {
    'part_1': 3,
    'part_2': 6,
}


@pytest.fixture
def answer():
    today = y25d01(auto_fetch=False)
    today.puzzle_raw = EXAMPLE
    today.parse_puzzle()
    today.solve()
    return today.answer


def test_answer_part_1(answer):
    assert answer['part_1'] == EXPECTED['part_1']


def test_answer_part_2(answer):
    assert answer['part_2'] == EXPECTED['part_2']
