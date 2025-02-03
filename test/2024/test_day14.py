import pytest
from Day14 import Day14


EXAMPLE = """\
p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3\
"""

EXPECTED = {
    'part_1': 12
}


@pytest.fixture
def today():
    today = Day14(auto_fetch=False)
    today.puzzle_raw = EXAMPLE
    today.parse_puzzle()
    return today


def test_answer_part_1(today):
    answer = today.solve_part_1(width=11, height=7)
    assert answer == EXPECTED['part_1']
