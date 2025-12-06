import pytest
from y25d05 import y25d05


EXAMPLE = """\
3-5
10-14
16-20
12-18

1
5
8
11
17
32\
"""


EXPECTED = {
    'part_1': 3,
    'part_2': 14,
}


@pytest.fixture
def answer():
    today = y25d05(auto_fetch=False)
    today.puzzle_raw = EXAMPLE
    today.parse_puzzle()
    today.solve()
    return today.answer


def test_answer_part_1(answer):
    assert answer['part_1'] == EXPECTED['part_1']


def test_answer_part_2(answer):
    assert answer['part_2'] == EXPECTED['part_2']
