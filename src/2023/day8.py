from day8_input import my_map, network
from math import lcm


class Node:
  def __init__(self, name, l, r):
    self.name = name
    self.LR = [l,r]

class Wasteland:
  def __init__(self):
    self.nodes = []

  def get_node_by_name(self, name):
    return list(filter(lambda n: n.name == name, self.nodes))[0]

  def get_nodes_by_char(self, nodes, char, index):
    return list(filter(lambda n: n.name[index] == char, nodes))

  def add_node(self, data):
    [name,l,r] = data
    self.nodes.append( Node(name, l, r))

  def link_nodes(self):
    for n in self.nodes:
      n.LR[0] = self.get_node_by_name(n.LR[0])
      n.LR[1] = self.get_node_by_name(n.LR[1])

  def travel(self, map_, from_, to_):
    n = self.get_node_by_name(from_)
    steps = 0
    while n.name != to_:
      n = n.LR[ map_[steps%len(map_)]]
      steps += 1
    return steps

class WastelandGhost:
  def __init__(self, nodes):
    self.nodes = nodes

  def get_index_by_name(self, name):
    return [i for i,n in enumerate(self.nodes) if n[0] == name][0]

  def get_index_by_char(self, char, index=-1):
    return [i for i,n in enumerate(self.nodes) if n[0][index] == char]

  def link_nodes(self):
    self.nodes = [[n,self.get_index_by_name(l),self.get_index_by_name(r)] for [n,l,r] in self.nodes]

  def get_loop_size(self, map_, from_, to_):
    MAP_SIZE = len(map_)
    n = self.get_index_by_name(from_)
    steps = 0
    while True:
      n = self.nodes[n][map_[steps%MAP_SIZE]]
      steps += 1
      if self.nodes[n][0][2] == to_:
        return steps

  def travel(self, map_, from_, to_):
    nodes = self.get_index_by_char(from_)
    loops = [self.get_loop_size( map_, self.nodes[n][0], to_) for n in nodes]
    return lcm(*loops)

if __name__ == '__main__':
  # Puzzle 1
  wasteland_o = Wasteland()
  for n in network:
    wasteland_o.add_node(n)
  wasteland_o.link_nodes()
  my_map = [0 if d=='L' else 1 for d in my_map]
  steps = wasteland_o.travel(my_map, 'AAA', 'ZZZ')
  print(f"Puzzle 1: {steps}")

  # Puzzle 2
  wasteland_o = WastelandGhost(network)
  wasteland_o.link_nodes()
  my_map = [m+1 for m in my_map]
  steps = wasteland_o.travel(my_map, 'A', 'Z')
  print(f"Puzzle 2: {steps}")
