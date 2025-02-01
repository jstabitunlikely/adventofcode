import pytest
from Day10 import Day10


EXAMPLE = """\
89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732\
"""

EXPECTED = {
    'part_1': 36,
    'part_2': 81,
}


@pytest.fixture
def answer():
    today = Day10(auto_fetch=False)
    today.puzzle_raw = EXAMPLE
    today.parse_puzzle()
    today.solve()
    return today.answer


def test_answer_part_1(answer):
    assert answer['part_1'] == EXPECTED['part_1']


def test_answer_part_2(answer):
    assert answer['part_2'] == EXPECTED['part_2']
