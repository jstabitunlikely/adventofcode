import re


card_re = re.compile(r'.+:(.+)\|(.+)')

with open("day4_input.txt", "r") as f:
    deck = f.read().splitlines()
    points = 0
    face_values = []
    for card in deck:
        winning_numbers = card_re.match(card).group(1).split(' ')
        winning_numbers = [n for n in winning_numbers if n]
        my_numbers = card_re.match(card).group(2).split(' ')
        my_numbers = [n for n in my_numbers if n]
        hits = sum([n in my_numbers for n in winning_numbers])
        face_values.append(hits)
        if hits:
            points += 2**(hits-1)
    print(points)

    card_cntr = [1]*len(face_values)
    for i, v in enumerate(face_values):
        fi = i + 1
        li = fi + v
        card_cntr[fi:li] = [n+card_cntr[i] for n in card_cntr[fi:li]]
    new_deck_size = sum(card_cntr)
    print(new_deck_size)
