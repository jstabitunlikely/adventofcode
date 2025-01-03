#!/usr/bin/python3

import re

import inputfetcher
from inputparsers import parse_matrix2d

EXAMPLE1 = """MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX"""

EXAMPLE2 = """.M.S......
..A..MSMS.
.M.S.MAA..
..A.ASMSM.
.M.S.M....
..........
S.S.S.S.S.
.A.A.A.A..
M.M.M.M.M.
.........."""


def parse_input(use_example1=False, use_example2=False):
    if use_example1:
        data = EXAMPLE1
    elif use_example2:
        data = EXAMPLE2
    else:
        data = inputfetcher.fetch_input('2024', '4')
    return parse_matrix2d(data, str)



def count_in_rows(textrix):
    xmas_re = re.compile(r"(?=XMAS|SAMX)")
    count = 0
    for row in textrix:
        count += len(re.findall(xmas_re, "".join(row)))
    return count


def transpose(l):
    return list(map(list, zip(*l)))


def solve_1(textrix):
    # horizontally
    xmas_hits = count_in_rows(textrix)

    # vertically
    xmas_hits += count_in_rows(transpose(textrix))

    # diagonally
    for i, row in enumerate(textrix[:-3]):
        textrix_lsh = [row]
        textrix_rsh = [row]
        for j in range(1, 4):
            textrix_lsh.append(textrix[i+j][j:] + j*['.'])  # shift left
            textrix_rsh.append(j*['.'] + textrix[i+j][:-j])  # shift right
        xmas_hits += count_in_rows(transpose(textrix_lsh))
        xmas_hits += count_in_rows(transpose(textrix_rsh))

    return xmas_hits


def solve_2(textrix):
    xmas_hits = 0
    for i in range(1, len(textrix)-1):
        for j in range(1, len(textrix[i])-1):
            if textrix[i][j] != 'A':
                continue
            else:
                x = textrix[i+1][j-1] + textrix[i-1][j-1] + \
                    textrix[i-1][j+1] + textrix[i+1][j+1]
                if x in ["MMSS", "MSSM", "SSMM", "SMMS"]:
                    xmas_hits += 1
    return xmas_hits


if __name__ == "__main__":
    textrix = parse_input()
    result_1 = solve_1(textrix)
    print(f'Result 1: {result_1}')
    result_2 = solve_2(textrix)
    print(f'Result 2: {result_2}')
