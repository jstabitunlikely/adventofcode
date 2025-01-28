# from day13_input import example as valley
from day13_input import puzzle_input as valley
from itertools import groupby
import numpy as np

MUL_H = 100
MUL_V = 1

# Valley into list of fields
fields = [list(group)
          for k, group in groupby(valley, lambda x: x == '') if not k]
# Translate symbols to numbers
to_num = str.maketrans({'#': '1', '.': '0'})
fields = [[f.translate(to_num) for f in field] for field in fields]
# Convert the strings to list of integers
fields = [[list(map(int, list(f))) for f in field] for field in fields]


def find_mirror(field, margin=0):
    for m, f in zip([MUL_H, MUL_V], [field, field.T]):
        for i,_ in enumerate(f[:-1], start=1):
            sample, behind = np.vsplit(f, [i])
            sample_reflection = np.flip(sample, axis=0)
            n = min(len(sample), len(behind))
            diff = np.abs(sample_reflection[:n] - behind[:n])
            if np.sum(diff) == margin:
                return m*(i)


def main():
    answer = sum([find_mirror(np.array(field), margin=0) for field in fields])
    print(f"Puzzle #1: {answer}")

    answer = sum([find_mirror(np.array(field), margin=1) for field in fields])
    print(f"Puzzle #2: {answer}")


if __name__ == '__main__':
    main()
