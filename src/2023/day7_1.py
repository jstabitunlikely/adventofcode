from collections import Counter
from day7_input import hands


# Map the face values to HEX numbers, so hands can be sorted easily
card_to_hex = str.maketrans({'T':'a', 'J':'b', 'Q':'c', 'K':'d', 'A':'e'})

# Simply look at how many matching cards we have
def get_hand_strength(counts):
  # five of a kind
  if counts.count(5):
    return 6
  # four of a kind
  elif counts.count(4):
    return 5
  # full house
  elif counts.count(3) and counts.count(2):
    return 4
  # three of a kind
  elif counts.count(3):
    return 3
  # two pairs
  elif counts.count(2) == 2:
    return 2
  # one pair
  elif counts.count(2) == 1:
    return 1
  # high cards
  else:
    return 0

# Getting the strength for the primary rule
hands_type = [get_hand_strength(list(Counter(h[0]).values())) for h in hands]

# Getting the order for the secondary rule
hands_order = [int(h[0].translate(card_to_hex), 16) for h in hands]

# Ranking
game = zip(hands, hands_type, hands_order)
game_sorted = sorted(game, key=lambda x: (x[1],x[2]))
hands_ranked, _, _ = zip(*game_sorted)

# Count the winnings
winnings = sum([(i+1)*bid for i,[_,bid] in enumerate(hands_ranked)])
print(winnings)
