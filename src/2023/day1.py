import re


word2number = {
    'one': '1',
    'two': '2',
    'three': '3',
    'four': '4',
    'five': '5',
    'six': '6',
    'seven': '7',
    'eight': '8',
    'nine': '9'
}

digit_re = re.compile(
    r'(?=([0-9]|one|two|three|four|five|six|seven|eight|nine))', re.I)


def line2num_2(line):
    matches = [m for m in digit_re.finditer(line)]
    d1 = matches[0].group(1)
    d2 = matches[-1].group(1)
    if not d1.isnumeric():
        d1 = word2number[d1]
    if not d2.isnumeric():
        d2 = word2number[d2]
    return int(d1+d2)


with open("day1_input.txt", "r") as f:
    print(sum([line2num_2(line) for line in f.read().splitlines()]))
