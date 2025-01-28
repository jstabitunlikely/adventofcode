from day9_input import data
import numpy as np


def predict( dataset):
    dn = [np.array( dataset)]
    while dn[-1].any():
        dn.append( np.diff( dn[-1], 1))
    prediction = [dn[-1] for dn in dn[-2::-1]]
    return sum( prediction)

# Puzzle 1
result = sum([predict(row) for row in data])
print(f"Puzzle 1: {result}")

# Puzzle 2
result = sum([predict(row[::-1]) for row in data])
print(f"Puzzle 2: {result}")
