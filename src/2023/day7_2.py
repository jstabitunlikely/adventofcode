from collections import Counter
from day7_input import hands

# Map the face values to HEX numbers, so hands can be sorted easily
card_to_hex = str.maketrans({'T':'a', 'J':'0', 'Q':'c', 'K':'d', 'A':'e'})

# Use the Jokers to increase the counters of other cards
# Starting with the highest count where they help the most
def use_jokers(counts, jokers):
  counts = sorted(counts, reverse=True)
  counts[0] += jokers
  return counts

# Simply look at how many matching cards we have
def get_hand_type(counts):
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

# Number of Jokers in each hand
hands_jokers = [Counter(h[0])['J'] for h in hands]
# Number of non-Joker cards in each hand
hands_wo_jokers = [Counter(h[0]) for h in hands]
for c in hands_wo_jokers:
    if 'J' in c:
        c['J'] = 0
hands_wo_jokers = [list(c.values()) for c in hands_wo_jokers]
# Number of cards after the Jokers were used as other cards
hands_w_jokers = [use_jokers(h,j) for h,j in zip(hands_wo_jokers, hands_jokers)]

# Getting the strength for the primary rule
hands_type = [get_hand_type(h) for h in hands_w_jokers]

# Getting the order for the secondary rule
hands_order = [int(h[0].translate(card_to_hex), 16) for h in hands]

# Ranking
game = zip(hands, hands_type, hands_order)
game_sorted = sorted(game, key=lambda x: (x[1],x[2]))
hands_ranked, _, _ = zip(*game_sorted)

# Count the winnings
winnings = sum([(i+1)*bid for i,[_,bid] in enumerate(hands_ranked)])
print(winnings)
