import math


def sign(num: int) -> int:
    if num < 0:
        return -1
    if num > 0:
        return 1
    return 0


def is_int(number,
           rel_tol=1e-9):
    return math.isclose(number, round(number), rel_tol=rel_tol)


def transpose(matrix):
    return list(map(list, zip(*matrix)))
