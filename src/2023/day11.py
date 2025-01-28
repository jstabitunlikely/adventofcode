from day11_input import data as universe
from itertools import combinations
import numpy as np


# Puzzle 1
EXPANSION_RATE = 2
# Puzzle 2
EXPANSION_RATE = 1_000_000

# Use integers instead of characters for easier math
universe = [row.replace(".", "0").replace("#", "1") for row in universe]
universe = [list(map(int, p)) for p in universe]
universe = np.ma.array(universe)

# Find galaxies
galaxies = np.asarray( np.where( universe)).T

# Expand the universe Horizontally and Vertically
for ax in range(0,2):
    void = np.ma.array( np.where( ~universe.any( axis = 1-ax)))
    for g in galaxies:
        void.mask = False
        void.mask[ np.where(void > g[ax])] = True
        g[ax] += (EXPANSION_RATE-1) * void.count()

# The distance between two coordinates
def get_distance(a, b):
    return np.sum( np.abs( np.subtract(a, b)))

# Sum the distances
distances = sum([get_distance(g,n) for g,n in list(combinations(galaxies, 2))])
print(f"Distance traveled: {distances}")
