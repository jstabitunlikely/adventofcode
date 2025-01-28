import re


bag = {'red':12, 'green':13, 'blue':14}

dice = re.compile(r'(?=((\d+) (red|green|blue)))')

with open("day2_input.txt", "r") as f:
    games = f.read().splitlines()
    result = 0
    for i, game in enumerate(games,1):
        result += i*int(all([int(m.group(2)) <= bag[m.group(3)] for m in dice.finditer(game)]))
    print(f'Answer 1: {result}')


r = re.compile(r'(?=((\d+) red))')
g = re.compile(r'(?=((\d+) green))')
b = re.compile(r'(?=((\d+) blue))')

with open("day2_input.txt", "r") as f:
    games = f.read().splitlines()
    result = 0
    for game in games:
        r_min = max([int(m.group(2)) for m in r.finditer(game)])
        g_min = max([int(m.group(2)) for m in g.finditer(game)])
        b_min = max([int(m.group(2)) for m in b.finditer(game)])
        result += (r_min * g_min * b_min)
    print(f'Answer 2: {result}')