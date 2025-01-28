from day10_example import example1, example2, example3, example4
from day10_input import data
import sys
sys.setrecursionlimit(128*128)


field = data

class Coordinate():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"({self.x},{self.y})"

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        return Coordinate(x, y)

    def __sub__(self, other):
        x = self.x - other.x
        y = self.y - other.y
        return Coordinate(x, y)

S = Coordinate(1, 0)
N = Coordinate(-1, 0)
W = Coordinate(0, -1)
E = Coordinate(0, 1)

compass = {
    '|': {N: S, S: N},
    '-': {W: E, E: W},
    'L': {N: E, E: N},
    'J': {W: N, N: W},
    '7': {W: S, S: W},
    'F': {S: E, E: S}
}

def goto_next(curr_pos, prev_pos, loop=[]):
    loop.append(prev_pos)
    pipe = field[curr_pos.x][curr_pos.y]
    if pipe == 'S':
        return loop
    from_ = prev_pos - curr_pos
    to_ = compass[pipe][from_]
    next_pos = (curr_pos + to_)
    return goto_next(next_pos, curr_pos, loop)

for x, row in enumerate(field):
    for y, pipe in enumerate(row):
        if field[x][y] == 'S':
            start = Coordinate(x, y)
print(f"Start: {start}")
curr_pos = Coordinate(64, 62)  # TODO
loop = goto_next(curr_pos, start)
print(f"Length of the loop: {len(loop)}")

# Tiles inside the loop
loop = sorted(loop, key=lambda a: (a.x, a.y))
tiles_inside = []
for x, row in enumerate(field):
    for y, pipe in enumerate(row):
        if Coordinate(x, y) in loop:
            continue
        # REVISIT continue if
        #   - tile is outside of the first/last pipe element of the row
        #   - no pipe elements in this row
        # This needs loop to be a list of lists (pipes per row)
        intersects = list(filter(lambda p: p.x == x and p.y > y and field[p.x][p.y] != '-', loop))
        intersects = list(map(lambda p: field[p.x][p.y], intersects))
        intersects = ''.join(intersects)
        intersects = intersects.replace('L7', 'X')
        intersects = intersects.replace('FJ', 'Y')
        if len(intersects) % 2:
            tiles_inside.append(Coordinate(x,y))
print(f"Number of tiles inside the loop: {len(tiles_inside)}")
