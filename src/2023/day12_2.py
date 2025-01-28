from day12_input import example, data
import re
import logging
logger = logging.getLogger(__name__)

console = logging.StreamHandler()
logger.addHandler(console)
logger.setLevel(logging.INFO)
# logger.setLevel(logging.DEBUG)

springs = example
# springs = data

spring_map = [r[0] for r in springs]
spring_groups = [r[1] for r in springs]

UNFOLD = 5

def is_node_invalid(node, pattern):
    if not pattern.match(node):
        return True
    if not node.count('?'):
        logger.debug(f"\tValid leaf: {node}")
    return False

def count_invalid_nodes(nodes, pattern):
    invalid = 0
    for n in nodes:
        if is_node_invalid(n, pattern):
            invalid += (2**n.count('?'))
            logger.debug(f"\tInvalid leaves in branch {n}: {2**n.count('?')}")
            continue
        cn = get_child_nodes(n)
        if cn:
            invalid += count_invalid_nodes(cn, pattern)
    return invalid

def get_child_nodes(node):
    i = node.find('?')
    if -1 == i:
        return []
    node0 = node[:i] + '.' + node[i+1:]
    node1 = node[:i] + '#' + node[i+1:]
    return [node0, node1]

valid_in_total = 0
for i, [row, group_sizes] in enumerate(zip(spring_map, spring_groups)):
    row = '?'.join([row] * UNFOLD)
    logger.debug(f"Row: {row}\nSizes: {group_sizes}")

    p_body = r""
    for gsize in group_sizes:
        p_body += r"(^|[.?]+?)[#?]{" + re.escape(str(gsize)) + r"}"
    p_body = r"(" + p_body + r"){" + re.escape(str(UNFOLD)) + r"}"
    p_end = r"[.?]*?$"
    p = p_body + p_end
    pattern = re.compile(p)
    logger.debug(f"Pattern: {pattern}")

    total_patterns = 2**row.count('?')
    invalid_patterns = count_invalid_nodes([row], pattern)
    valid_patterns = total_patterns - invalid_patterns
    logger.info(f"\t{i} -> total: {total_patterns} -> invalid: {invalid_patterns} -> valid: {valid_patterns}")
    valid_in_total += valid_patterns

logger.info(f"Valid: {valid_in_total}")
