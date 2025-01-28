from collections import Counter
from day7_input import hands


card_to_hex = str.maketrans({'T':'a', 'J':'b', 'Q':'c', 'K':'d', 'A':'e'})
def get_hand_strength(counts):
  if counts.count(5):
    return 6
  elif counts.count(4):
    return 5
  elif counts.count(3) and counts.count(2):
    return 4
  elif counts.count(3):
    return 3
  elif counts.count(2) == 2:
    return 2
  elif counts.count(2) == 1:
    return 1
  return 0
hands_strength = [get_hand_strength(list(Counter(h[0]).values())) for h in hands]
hands_order = [int(h[0].translate(card_to_hex), 16) for h in hands]
game_sorted = sorted(zip(hands, hands_strength, hands_order), key=lambda x: (x[1],x[2]))
hands_ranked, _, _ = zip(*game_sorted)
print(sum([(i+1)*bid for i,[_,bid] in enumerate(hands_ranked)]))
