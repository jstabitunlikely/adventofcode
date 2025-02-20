import pytest
from Day22 import Day22


EXAMPLE_1 = """\
1
10
100
2024\
"""

EXAMPLE_2 = """\
1
2
3
2024\
"""

EXPECTED = {
    'part_1': 37327623,
    'part_2': 23
}


@pytest.fixture
def today():
    today = Day22(auto_fetch=False)
    today.puzzle_raw = EXAMPLE_1
    today.parse_puzzle()
    return today


def test_answer_part_1(today):
    today.solve()
    assert today.answer['part_1'] == EXPECTED['part_1']


def test_answer_part_1_cpu(today):
    part_1 = today.solve_part_1_cpu()
    assert part_1 == EXPECTED['part_1']


def test_answer_part_2(today):
    today.puzzle_raw = EXAMPLE_2
    today.parse_puzzle()
    today.solve()
    assert today.answer['part_2'] == EXPECTED['part_2']
