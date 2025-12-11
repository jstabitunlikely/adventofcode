import pytest
from y25d11 import y25d11


EXAMPLE1 = """\
aaa: you hhh
you: bbb ccc
bbb: ddd eee
ccc: ddd eee fff
ddd: ggg
eee: out
fff: out
ggg: out
hhh: ccc fff iii
iii: out\
"""

EXAMPLE2 = """\
svr: aaa bbb
aaa: fft
fft: ccc
bbb: tty
tty: ccc
ccc: ddd eee
ddd: hub
hub: fff
eee: dac
dac: fff
fff: ggg hhh
ggg: out
hhh: out\
"""


EXPECTED = {
    'part_1': 5,
    'part_2': 2,
}


@pytest.fixture
def answer():
    today = y25d11(auto_fetch=False)
    # Part 1
    today.puzzle_raw = EXAMPLE1
    today.parse_puzzle()
    part_1 = today.solve_part_1()
    # Part 2
    today.puzzle_raw = EXAMPLE2
    today.parse_puzzle()
    part_2 = today.solve_part_2()
    # Complete answer
    today.answer['part_1'] = part_1
    today.answer['part_2'] = part_2
    return today.answer


def test_answer_part_1(answer):
    assert answer['part_1'] == EXPECTED['part_1']


def test_answer_part_2(answer):
    assert answer['part_2'] == EXPECTED['part_2']
