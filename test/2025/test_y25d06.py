import pytest
from y25d06 import y25d06


EXAMPLE = """\
123 328  51 64
 45 64  387 23
  6 98  215 314
*   +   *   +  \
"""


EXPECTED = {
    'part_1': 4277556,
    'part_2': 0,
}


@pytest.fixture
def answer():
    today = y25d06(auto_fetch=False)
    today.puzzle_raw = EXAMPLE
    today.parse_puzzle()
    today.solve()
    return today.answer


def test_answer_part_1(answer):
    assert answer['part_1'] == EXPECTED['part_1']


def test_answer_part_2(answer):
    assert answer['part_2'] == EXPECTED['part_2']
