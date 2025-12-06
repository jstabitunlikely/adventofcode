import pytest
from y25d03 import y25d03


EXAMPLE = """\
987654321111111
811111111111119
234234234234278
818181911112111\
"""


EXPECTED = {
    'part_1': 357,
    'part_2': 3121910778619,
}


@pytest.fixture
def answer():
    today = y25d03(auto_fetch=False)
    today.puzzle_raw = EXAMPLE
    today.parse_puzzle()
    today.solve()
    return today.answer


def test_answer_part_1(answer):
    assert answer['part_1'] == EXPECTED['part_1']


def test_answer_part_2(answer):
    assert answer['part_2'] == EXPECTED['part_2']
