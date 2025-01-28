import re
from itertools import product

# 1
symbols = re.compile(r'[^0-9.]')
numbers_re = re.compile(r'[0-9]+')

with open("day3_input.txt", "r") as f:
    lines = f.read().splitlines()
    symbol_map = [[0 for x in range(len(lines[0]))] for y in range(len(lines))]

    for x, line in enumerate(lines):
        for y in [m.start() for m in symbols.finditer(line)]:
            for j, k in product(range(-1, 2), range(-1, 2)):
                symbol_map[x+j][y+k] = 1

    result = 0
    for x, line in enumerate(lines):
        for y1, y2, num in [(m.start(), m.end()-1, int(m.group(0))) for m in numbers_re.finditer(line)]:
            if any([symbol_map[x][y1], symbol_map[x][y2]]):
                result += num
    print(result)

# 2
gear_re = re.compile(r'\*')
numbers_re = re.compile(r'[0-9]+')

with open("day3_input.txt", "r") as f:
    lines = f.read().splitlines()
    gears = []
    numbers = []
    sum = 0
    for x, row in enumerate(lines):
        for y in [m.start() for m in gear_re.finditer(row)]:
            gears.append((x, y))
        for y1, y2, num in [(m.start(), m.end(), int(m.group(0))) for m in numbers_re.finditer(row)]:
            numbers.append((x,y1,y2-1,num))
    for gear in gears:
        nums = [int(n[3]) for n in numbers if (
             gear[0]-2 < n[0] < gear[0]+2 and
            (gear[1]-2 < n[1] < gear[1]+2 or
             gear[1]-2 < n[2] < gear[1]+2))
        ]
        if 2 == len(nums):
            sum += nums[0] * nums[1]
    print(sum)