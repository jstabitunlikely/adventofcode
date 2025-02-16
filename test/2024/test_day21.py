import pytest
from Day21 import Day21


EXAMPLE = """\
029A
980A
179A
456A
379A\
"""

EXPECTED = {
    'part_1': 126384,
    'part_2': 154115708116294
}


@pytest.fixture
def answer():
    today = Day21(auto_fetch=False)
    today.puzzle_raw = EXAMPLE
    today.parse_puzzle()
    today.solve()
    return today.answer


def test_answer_part_1(answer):
    assert answer['part_1'] == EXPECTED['part_1']


def test_answer_part_2(answer):
    assert answer['part_2'] == EXPECTED['part_2']
