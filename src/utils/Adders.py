import networkx as nx
import matplotlib.pyplot as plt


class Adders:

    def __init__(self) -> None:
        self.dags = [
            self.dag_half_adder(),
            self.dag_full_adder(),
            self.dag_ripple_carry_adder(5),
        ]

    def dag_half_adder(self) -> nx.DiGraph:

        dag = nx.DiGraph()

        # Input nodes
        dag.add_node('X', layer=0)
        dag.add_node('Y', layer=0)

        # XOR gate
        dag.add_node('XOR', layer=1)
        dag.add_edge('X', 'XOR')
        dag.add_edge('Y', 'XOR')

        # AND gate
        dag.add_node('AND', layer=1)
        dag.add_edge('X', 'AND')
        dag.add_edge('Y', 'AND')

        # Output nodes
        dag.add_node('Sum', layer=2)
        dag.add_edge('XOR', 'Sum')
        dag.add_node('Cout', layer=2)
        dag.add_edge('AND', 'Cout')

        # Give a label to nodes that doesn't have one
        self.do_label_nodes(dag)

        return dag

    def dag_full_adder(self) -> nx.DiGraph:
        dag = nx.DiGraph()

        # Inputs
        dag.add_nodes_from(['X', 'Y', 'Cin'])

        # XOR gates
        dag.add_node('XOR1', label='XOR')
        dag.add_node('XOR2', label='XOR')
        dag.add_edges_from([('X', 'XOR1'), ('Y', 'XOR1'),
                            ('XOR1', 'XOR2'), ('Cin', 'XOR2')])

        # AND gates
        dag.add_node('AND1', label='AND')
        dag.add_node('AND2', label='AND')
        dag.add_node('AND3', label='AND')
        dag.add_edges_from([('X', 'AND1'), ('Y', 'AND1'),
                            ('X', 'AND2'), ('Cin', 'AND2'),
                            ('Y', 'AND3'), ('Cin', 'AND3')])

        # OR gate
        dag.add_node('OR', label='OR')
        dag.add_edges_from([('AND1', 'OR'), ('AND2', 'OR'), ('AND3', 'OR')])

        # Outputs
        dag.add_nodes_from(['Sum', 'Cout'])
        dag.add_nodes_from(['Sum', 'Cout'])
        dag.add_edges_from([('XOR2', 'Sum'), ('OR', 'Cout')])

        self.do_label_nodes(dag)

        self.do_topological_ordering(dag)

        return dag

    def dag_ripple_carry_adder(self, num_bits: int) -> nx.DiGraph:
        dag = nx.DiGraph()

        # Add input nodes for the two operands and carry-in
        for i in range(num_bits):
            dag.add_node(f"X_{i}", layer=0)
            dag.add_node(f"Y_{i}", layer=0)

        # Add half adder node at the bottom
        dag.add_node(f"HA_0", layer=1)

        # Add full adder nodes for the rest of the bits
        for i in range(1, num_bits):
            dag.add_node(f"FA_{i}", layer=1)

        # Add output nodes for sum and carry-out
        for i in range(num_bits):
            dag.add_node(f"S_{i}", layer=2)

        Cout = f"S_{i+1}"
        dag.add_node(Cout, layer=2)

        # Connect input nodes to half adder
        dag.add_edge(f"X_0", f"HA_0")
        dag.add_edge(f"Y_0", f"HA_0")

        # Connect input nodes to full adders
        for i in range(1, num_bits):
            dag.add_edge(f"X_{i}", f"FA_{i}")
            dag.add_edge(f"Y_{i}", f"FA_{i}")

        # Connect half adders to sum and carry-out nodes
        dag.add_edge(f"HA_0", f"S_0")
        dag.add_edge(f"HA_0", f"FA_1")

        # Connect full adders to sum and carry-out nodes
        for i in range(1, num_bits):
            dag.add_edge(f"FA_{i}", f"S_{i}")
            if i < num_bits - 1:
                dag.add_edge(f"FA_{i}", f"FA_{i+1}")

        dag.add_edge(f"FA_{num_bits-1}", Cout)

        # Give a label to nodes that doesn't have one
        self.do_label_nodes(dag)

        return dag

    def do_topological_ordering(self, dag: nx.DiGraph) -> None:
        generations = list(nx.topological_generations(dag))
        for layer, nodes in enumerate(generations):
            for node in nodes:
                dag.nodes[node]["layer"] = layer

    def do_label_nodes(self, dag: nx.DiGraph) -> None:
        for n in dag.nodes():
            if 'label' not in dag.nodes[n]:
                dag.nodes[n]['label'] = n

    def visualize(self) -> None:
        for dag in self.dags:
            pos = nx.multipartite_layout(dag, subset_key="layer", align="horizontal")
            fig, ax = plt.subplots()
            fig.set_figheight(6)
            fig.set_figwidth(12)
            nx.draw_networkx_nodes(G=dag, pos=pos, ax=ax, node_shape="s", node_size=800)
            nx.draw_networkx_edges(G=dag, pos=pos, ax=ax, node_shape="s", node_size=800)
            node_labels = dict(dag.nodes(data='label'))  # type:ignore
            nx.draw_networkx_labels(G=dag, pos=pos, ax=ax, font_size=10, labels=node_labels)
            dag.nodes()
        plt.show()


adders = Adders()
adders.visualize()
