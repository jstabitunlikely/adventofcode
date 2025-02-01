import pytest
from Day09 import Day09


EXAMPLE = """\
2333133121414131402\
"""

EXPECTED = {
    'part_1': 1928,
    'part_2': 2858,
}


@pytest.fixture
def answer():
    today = Day09(auto_fetch=False)
    today.puzzle_raw = EXAMPLE
    today.parse_puzzle()
    today.solve()
    return today.answer


def test_answer_part_1(answer):
    assert answer['part_1'] == EXPECTED['part_1']


def test_answer_part_2(answer):
    assert answer['part_2'] == EXPECTED['part_2']
