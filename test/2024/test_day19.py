import pytest
from Day19 import Day19


EXAMPLE = """\
r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb\
"""

EXPECTED = {
    'part_1': 6,
    'part_2': 16
}


@pytest.fixture
def answer():
    today = Day19(auto_fetch=False)
    today.puzzle_raw = EXAMPLE
    today.parse_puzzle()
    today.solve()
    return today.answer


def test_answer_part_1(answer):
    assert answer['part_1'] == EXPECTED['part_1']


def test_answer_part_2(answer):
    assert answer['part_2'] == EXPECTED['part_2']
