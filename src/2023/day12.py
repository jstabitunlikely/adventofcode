from day12_input import example, data
import logging
logger = logging.getLogger(__name__)

console = logging.StreamHandler()
logger.addHandler(console)
logger.setLevel(logging.INFO)
# logger.setLevel(logging.DEBUG)

springs = example
# springs = data

def bit_count(self):
    return bin(self).count("1")

spring_map = [r[0] for r in springs]
spring_map = [s.replace('#', '1') for s in spring_map]
spring_map = [s.replace('.', '0') for s in spring_map]
spring_groups = [r[1] for r in springs]

# ==================
# Puzzle 2 mod
# ==================
# spring_map = [s*5 for s in spring_map]
# spring_groups = [s*5 for s in spring_groups]
# ==================

valid_arrangements = 0
for [pattern, sizes] in zip(spring_map, spring_groups):
    logger.debug(f"{pattern}, {sizes}")

    # Calculate how many options we have altogether
    unknown_total = pattern.count('?')
    damaged_total = sum(sizes)
    damaged_known = pattern.count('1')
    damaged_unknown = damaged_total - damaged_known
    logger.debug(f"\t-> Possibilities in total : {2**unknown_total}")

    # Narrow it down a bit by using the total number of damaged parts
    candidates_encoded = [i for i in range(2**unknown_total) if bit_count(i) == damaged_unknown]

    # Decode the candidates
    wildcard_indices = [i for i, c in enumerate(pattern) if c == '?']
    candidates_decoded = []
    for wc in candidates_encoded:
        wc_bin = format(wc, '0' + str(unknown_total) + 'b')
        candidate = pattern
        for i, wci in enumerate(wildcard_indices[::-1]):
            candidate = candidate[:wci] + candidate[wci:].replace(candidate[wci], wc_bin[i], 1)
        candidates_decoded.append(candidate)
    logger.debug(f"\t-> Valid candidates: {len(candidates_decoded)}")

    assert len(candidates_decoded) == len(set(candidates_decoded)), f"{candidates_decoded}"

    # Check candidates against the constraints
    candidates_passing = []
    for c in candidates_decoded:
        c_groups = c.split('0')
        c_groups = [g for g in c_groups if g]
        # Number of the groups
        if len(sizes) != len(c_groups):
            continue
        for s,c in zip(sizes,c_groups):
            if s != c.count('1'):
                break
        else:
            candidates_passing.append(candidate)
        continue
    logger.debug(f"\t-> Candidates passing: {len(candidates_passing)}")
    valid_arrangements += len(candidates_passing)

logger.info(valid_arrangements)
