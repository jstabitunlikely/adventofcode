import pytest
from Day17 import Day17


EXAMPLE = """\
Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0\
"""

EXPECTED = {
    'part_1': '4,6,3,5,6,3,5,2,1,0',
}


@pytest.fixture
def answer():
    today = Day17(auto_fetch=False)
    today.puzzle_raw = EXAMPLE
    today.parse_puzzle()
    answer = today.solve_part_1()
    return answer


def test_answer_part_1(answer):
    assert answer == EXPECTED['part_1']
